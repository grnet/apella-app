import Ember from 'ember';
import _ from 'lodash/lodash';


const {
  get,
} = Ember;

function can_create_for_type(app_list, app_type) {
    let apps = _.filter(app_list, function(o) {
      return o && get(o.getRecord(), 'app_type') === app_type;
    });
    // sort by id
    apps = _.sortBy(apps, ['id']);
    // get latest application for given app_type
    let latest = _.last(apps);
    if (latest) {
      let {
        state: as,
        position_state: ps
      } = latest.getRecord().getProperties(['state', 'position_state']);

      // logic for latest application
      // cannot apply for an application if
      // state = pending or the application position is in an ongoing or
      // successful status
      if (as === 'pending' ||
          ['posted', 'electing', 'successful'].includes(ps) ||
          (as === 'approved' && !ps)) {
        return false;
      }
    }
    return true;
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
// can_create_application() will return an object:
// {
//  'can_create_tenure': <True | False>,
//  'can_create_renewal': <True | False>
// }
function can_create(app_list) {
  let res = {
    'can_create_tenure': true,
    'can_create_renewal': true
  };

  if (app_list && app_list.length > 0) {
    res['can_create_tenure'] = can_create_for_type(app_list, 'tenure');
    res['can_create_renewal'] = can_create_for_type(app_list, 'renewal');
  }
  return res;
}

export {
  can_create
};

