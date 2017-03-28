import {ApellaGen} from 'ui/lib/common';
import {field} from 'ember-gen';

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
  },

  list: {
    page: {
      title: 'user_application.menu_label'
    },
    menu: {
      icon: 'trending_up',
       label: 'user_application.menu_label'
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
          field('updated_at_format', {label: 'updated_at.label'})
        ];
        if (role === 'professor' || role === 'candidate') {
          fields.splice(0, 2);
        }
        return fields;
      })
    }
  },
});
