import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import _ from 'lodash/lodash'
import Users  from 'ui/gen/user';

let {
  computed, get
} = Ember;

let members = Users.extend({
  create: {
    page: {
      toolbar: {
        display: false
      }
    }
  },
  list: {
    /*
     * ToDo
     * This in the future should be moved to getModel (registry.get('members'))
     */
    processModel(users) {
      return users.then( () => {
        // URL format: domain/resource_plural/id/
        let members_urls =  this.getParentModel().get('members').getEach('id');
        let members_ids = members_urls.map((i) => {
          // split url by '/' and get the last element of the array
          return _.last( _.words(i));
        })
          return users.filter((user) => {
            let id = user.get('id');
            return members_ids.indexOf(id) > -1;
          });
      });
    },
    layout: 'table',
    sortBy: 'id:asc',
    fields: [
      field('id', {label: 'common.id_label', type: 'text'}),
      field('username', {label: 'username.label', type: 'text'}),
      field('role_verbose', {label: 'role.label', type: 'text'}),
    ],
    row: {
      actions: ['gen:details']
    }
  }
});

export default gen.CRUDGen.extend({
  modelName: 'registry',
  path: 'registries',

  common: {
    fieldsets: [{
      label: 'registry.main_section.title',
      fields: [field('type', {label: 'common.type_label'}), 'department'],
      layout: {
        flex: [30, 70]
      }
    },{
      label: 'registry.members_section.title',
      fields: ['members']
    }]
  },

  list: {
    menu: {
      icon: 'view list',
      label: 'registry.menu_label'
    },
    layout: 'table',
    sortBy: 'institution.title:asc',
    page: {
     title: 'registry.menu_label'
    },
    fields: [
      field('institution.title', {label: 'institution.label', type: 'text'}),
      field('department.title', {label: 'department.label', type: 'text'}),
      field('type_verbose', {label: 'common.type_label', type: 'text'})
    ],
    row: {
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  create: {
    page: {
      title: 'common.create_label'
    },
    menu: {
      label: 'common.button.create_label',
      icon: 'library add'
    }
  },
  details: {
    menu: {
      label: 'common.button.details_label',
      icon: 'remove red eye'
    }
  },
  record: {
    menu: {
      label: computed('model.id', function() {
        return get(this, 'model.id');
      })
    },
  },
  edit: {
    page: {
      title: 'common.edit_label'
    },
    menu: {
      label: 'common.button.edit_label',
      icon: 'border color'
    }
  },
  nested: {
    members: members
  }
});
