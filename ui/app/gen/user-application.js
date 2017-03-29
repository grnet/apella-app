import {ApellaGen} from 'ui/lib/common';
import {field} from 'ember-gen';
import {acceptApplication, rejectApplication} from 'ui/utils/common/actions';

const {
  computed,
  get
} = Ember;

export default ApellaGen.extend({
  order: 1600,
  modelName: 'user_application',
  auth: true,
  path: 'user-applications',
  session: Ember.inject.service(),

  abilityStates: {
    can_create: computed('role', 'user.rank', 'user.is_foreign', function() {
      let role = get(this, 'role'),
          rank = get(this, 'user.rank'),
          domestic = !get(this, 'user.is_foreign');
      let professor = role === 'professor',
          tenured = rank === 'Tenured Assistant Professor';
      return professor && domestic && tenured;
    }),
    owned: computed('', function(){
      return true;
    })
  },

  list: {
    page: {
      title: 'user_application.menu_label'
    },
    menu: {
      icon: 'trending_up',
      label: computed('role', function() {
        let role = get(this, 'role');
        if (role === 'professor'){
          return 'my_user_application.menu_label';
        }
        else {
          return 'user_application.menu_label';
        }
      }),
    },
    filter: {
      active: true,
      serverSide: true,
      search: false,
      meta: {
        fields: ['state', 'app_type' ]
      },
    },
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let fields = [
          field('user.id', {label: 'user_id.label'}),
          field('user.full_name_current', {label: 'full_name_current.label'}),
          field('state_verbose', {label: 'state.label'}),
          field('app_type_verbose', {label: 'app_type.label'}),
          field('created_at_format', {label: 'created_at.label'}),
        ];
        if (role === 'professor' || role === 'candidate') {
          fields.splice(0, 2);
        }
        return fields;
      }),
      actions: ['gen:details', 'acceptApplication', 'rejectApplication'],
      actionsMap: {
        acceptApplication: acceptApplication,
        rejectApplication: rejectApplication,
      }
    }
  },
  details: {
    page: {
      title: computed.readOnly('model.app_type_verbose')
    },
    fieldsets: [{
      label: 'fieldsets.labels.user_application',
      fields: computed('role', function(){
        let role = get(this, 'role');
        let fields = [
          field('user.id', {label: 'user_id.label'}),
          field('user.full_name_current', {label: 'full_name_current.label'}),
          field('state_verbose', {label: 'state.label'}),
          field('app_type_verbose', {label: 'app_type.label'}),
          field('created_at_format', {label: 'created_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'}),
        ];
        if (role === 'professor' || role === 'candidate') {
          fields.splice(0, 2);
        }
        return fields;
      }),
      layout: {
        flex: [50, 50, 50, 50, 50, 50]
      }
    }]
  }
});
