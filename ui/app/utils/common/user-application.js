import Ember from 'ember';
import _ from 'lodash/lodash';


const {
  get,
} = Ember;


function can_create(app_list) {
  const types = ['electing', 'posted', 'successful'];
  let memo = {
    can_create_renewal: true,
    can_create_tenure: true
  };

  let groups = _.groupBy(app_list, (item) => {
    return get(item.getRecord(), 'app_type');
  });

  _.each(_.keys(groups), (group) => {
      const key = `can_create_${group}`;
      let pending = _.filter(groups[group], (record) => {
        return (get(record.getRecord(), 'state') === 'pending');
      }).length;

      let approved = _.filter(groups[group], (record) => {
        const state = get(record.getRecord(), 'state');
        const position_state = get(record.getRecord(), 'position_state')
        return (state === 'approved') && ((position_state === null) || types.includes(position_state));
      }).length;
      memo[key] = (pending > 0 || approved > 0) ? false : true;
  });

  return memo;

}

export {
  can_create
};

