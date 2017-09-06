import {field} from 'ember-gen';
import {ApellaGen, urlValidator} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import PROFESSOR from 'ui/utils/common/professor';
import {afterDays} from 'ui/validators/dates';

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

export default ApellaGen.extend({
  order: 2000,
  name: 'leaves',
  modelName: 'professor',
  resourceName: 'professors',
  auth: true,
  path: 'leaves',

  common: {
    validators: {
      leave_ends_at: [afterDays({on:'leave_starts_at', days:2})],
    }
  },

  list : {
    getModel: function(params) {
      params = params || {};
      params.is_verified = true;
      params.is_active = true;
      let role = get(this, 'session.session.authenticated.role');

      if (role === 'institutionmanager') {
        let inst = get(this, 'session.session.authenticated.institution');
        let id = inst.split('/').slice(-2)[0];
        params.institution = id;
        return this.store.query('professor', params);
      }

      if (role === 'assistant') {
        let deps = get(this, 'session.session.authenticated.departments');

        let promises = deps.map((id) => {
          params.department = id;
          return this.store.query('professor', params);
        })

        var promise = Ember.RSVP.all(promises).then(function(arrays) {
          var mergedArray = Ember.A();
          arrays.forEach(function (records) {
            mergedArray.pushObjects(records.toArray());
          });
          return mergedArray;
        });

        return DS.PromiseArray.create({
          promise: promise,
        });


      }
    },
    page: {
      title: 'leaves.menu_label',
    },
    menu: {
      icon: 'work',
      label: 'leaves.menu_label',
      display: computed('role', function(){
        let role = get(this, 'role');
        let is_secretary = get(this, 'session.session.authenticated.is_secretary');
        return is_secretary || role === 'institutionmanager';
      }),
    },
    row: {
      fields: [
        'user_id',
        'full_name_current',
        'department.title_current',
        'rank_verbose',
        'leave_starts_at_format',
        'leave_ends_at_format',
        'on_leave_verbose',
      ],
      actions: ['gen:details', 'gen:edit'],
    },
    filter: {
      active: false,
      serverSide: true,
      search: true,
    },
    sort: {
      active: true,
      serverSide: true,
      sortBy: 'user_id',
      fields: [
        'user_id',
      ]
    },

  },

  details: {
    page: {
      title: computed.readOnly('model.full_name_current')
    },
    fieldsets: [
      PROFESSOR.LEAVE_FIELDSET_DETAILS,
    ],
  },

  edit: {
    fieldsets: [
      PROFESSOR.LEAVE_FIELDSET_EDIT,
    ],
  },

});
