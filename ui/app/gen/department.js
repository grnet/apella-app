import {ApellaGen, i18nField} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';
import {field} from 'ember-gen';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';

const {
  get,
  computed
} = Ember;

const subjectsField = field('subjects', {
  /*
   * Custom table query.
   *
   * store is the store service
   * params is the table-requested params (if any) such as ordering/offset/limit/filters etc.
   * value is the value of the field on the bound model (in this case it is not used)
   */
  valueQuery: function(store, params, value) {
    return store.query('subject', params);
  },

  // a list-like gen config
  modelMeta: {
    row: {
      fields: [i18nField('title'), i18nField('area.title')],
      actions: ['view'],
      actionsMap: {
        view: {
          primary: true,
          action: function(route, model) {
            model.set('_inProgress', true);
            Ember.run.later(function() {
              model.toggleProperty('_inProgress');
              route.transitionTo('subject.record.index', model);
            }, 1500);
          },
          permissions: [{
            resource: 'subject',
            action: 'view'
          }],
          label: computed('model.title_current', function() {
            return 'view subject: ' + get(this, 'model.title_current')
          }),
          confirm: true,
          prompt: {
            title: 'are you sure??',
            message: 'are you sure you want to visit the subject?',
            ok: 'go',
            cancel: 'cancel',
          },
          spin: computed.reads('model._inProgress'),
          icon: computed('model._inProgress', function() {
            if (get(this, 'model._inProgress')) {
              return 'speaker_phone';
            }
            return 'visibility'
          })
        }
      }
    },
    paginate: {
      active: true,
      serverSide: true,
      limits: [5, 10, 15]
    },
    filter: {
      search: true,
      serverSide: true,
      active: true,
      meta: {
        fields: [i18nField('title'), 'area']
      }
    },
    sort: {
      serverSide: true,
      active: true,
      fields: ['title'] 
    }
  },
  modelName: 'subject',
  dataKey: 'title',
  displayComponent: 'gen-display-field-table'
});

export default ApellaGen.extend({
  modelName: 'department',
  auth: true,
  path: 'departments',
  session: Ember.inject.service(),

  common: {
    proloadModels: ['institution', 'department'],
    validators: {
      title: [i18nValidate([validate.presence(true), validate.length({min:4, max:50})])],
      dep_number: [validate.presence(true), validate.number({integer: true})]
    }
  },
  list: {
    menu: {
      icon: 'domain',
      label: 'department.menu_label',
      display: computed(function() {
        let role = get(this, 'session.session.authenticated.role');
        let permittedRoles = ['helpdeskuser', 'helpdeskadmin', 'institutionmanager'];
        return (permittedRoles.includes(role) ? true : false);
      })
    },
    page: {
      title: 'department.menu_label',
    },
    layout: 'table',
    sortBy: 'title_current:asc',
    row: {
      fields: ['title_current', field('school.title_current', {label: 'school.label', type: 'text'}), 'institution.title_current'],
      actions: ['gen:details', 'gen:edit', 'remove']
    }
  },
  details: {
//    fields: ['title_current', subjectsField],
      fields: ['title_current', 'school.title_current', 'institution.title_current',
        'dep_number'],
    page: {
      title: computed.readOnly('model.title_current')
    },
  },
  create: {
    onSubmit(model) {
      this.transitionTo('department.record.index', model)
    }
  }
});
