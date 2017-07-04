import Ember from 'ember';
import _ from 'lodash/lodash';


const {
  get,
} = Ember;

const sort_by_id = _.partial(_.sortBy, _, ['id']);
const latest = _.compose(_.last, sort_by_id);
const APP_TYPES = ['renewal', 'tenure'];


function latest_for_type(app_list, app_type) {

    let apps = _.filter(app_list, function(o) {
      return o && get(o.getRecord(), 'app_type') === app_type;
    });

    if (apps.length >0 ) {
      return latest(apps).getRecord().getProperties(['state', 'position_state']);
    } else {
      return {
        state: null,
        position_state: null
      }
    }
}

// Helper to resolve if a professor can create a new application
//
// Given an application list (app_list) where the elements are expected to
// be objects with at least the following keys:
// {
//  'state': <pending | accepted | rejected>,
//  'app_type': <tenure | renewal>,
//  'position_state': <null | posted | electing | successful | failed | cancelled>
// }
// can_create() will return an object with keys `can_create_${app_type}` and
// boolean values
function can_create(app_list) {

  // Cannot apply for an application if state = pending or the
  // application position is in an ongoing or successful status
  return  _.reduce(APP_TYPES, function(memo, app_type ){
    if (app_list && app_list.length > 0) {
      let {state: as, position_state: ps} = latest_for_type(app_list, app_type);
      memo[`can_create_${app_type}`] = !( (as === 'pending' ||
          ['posted', 'electing', 'successful'].includes(ps) ||
          (as === 'approved' && !ps)) )
    } else {
      memo[`can_create_${app_type}`] = true;
    }
    return memo;
  }, {});

}

export {
  can_create
};

