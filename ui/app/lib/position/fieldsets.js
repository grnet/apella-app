import {field} from 'ember-gen';
import {disable_field, i18nField} from 'ui/utils/common/fields';
import moment from 'moment';
import {
  candidaciesField, committeeElectorsField, historyField,
  contactField
} from 'ui/lib/position/table_fields';

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

const  position = {
  create: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: ['title',
        field('department', {
          autocomplete: true,
          query: function(table, store, field, params) {

            // If the logged in user is an assistant, department field is a
            // select list  with the assistant's departments
            let role = get(field, 'session.session.authenticated.role');
            if (role == 'assistant') {
              let deps = get(field, 'session.session.authenticated.departments');
              let promises = deps.map((url) => {
                let id = url.split('/').slice(-2)[0];
                return store.findRecord('department', id);
              })

              var promise = Ember.RSVP.all(promises).then((res) => {
                return res;
              }, (error) => {
                return [];
              });

              return DS.PromiseArray.create({
                promise : promise
              })
            }

            // on load sort by title
            let locale = get(table, 'i18n.locale');
            let ordering_param = {
              ordering: `title__${locale}`
            };
            let query;
            // If the logged in user is an institutionmanager, department field
            // is a select list with all the deparments that belong to the
            // institutionmanager's institution
            if (role == 'institutionmanager') {
              let user_institution = get(field, 'session.session.authenticated.institution');
              let id = user_institution.split('/').slice(-2)[0];
              query = assign({}, { institution: id }, ordering_param);
            } else {
              query = ordering_param;
            }
            return store.query('department', query);
          }
        }),
        'description',
        'discipline','subject_area', 'subject'],
      layout: {
        flex: [50, 50, 100, 100, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }
  },
  details: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: ['code', 'state_calc_verbose', 'title',
        field('department.title_current', {label: 'department.label'}),
        'department.institution.title_current',
        'discipline', 'description', field('subject_area.title_current',{label: 'subject_area.label'}),
        field('subject.title_current', {label: 'subject.label'})],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 100, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: ['fek', field('fek_posted_at_format', {label: 'fek_posted_at.label'}),
        field('starts_at_format', {label: 'starts_at.label'}),
        field('ends_at_format', {label: 'ends_at.label'})],
      layout: {
        flex: [50, 50, 50, 50]
      }
    },
    candidacies: {
      label: 'candidacy.menu_label',
      fields: [candidaciesField]
    },
    committee: {
      label: 'committee_members.label',
      fields: [
        committeeElectorsField('committee_internal', 'internal'),
        committeeElectorsField('committee_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_regular: {
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', 'internal'),
        committeeElectorsField('electors_regular_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_substitite: {
      label: 'electors_substitute_members.label',
      fields: [
        committeeElectorsField('electors_substitute_internal', 'internal'),
        committeeElectorsField('electors_substitute_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    history: {
      label: 'position.history.title',
      fields: [historyField]
    }
  },
  edit: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: computed('role', 'state', function() {
        let role = get(this, 'role'),
          state = get(this, 'model.state'),
          title, department, description, discipline, subject_area, subject;
        if((role === 'helpdeskadmin' || role === 'helpdeskuser') && state === 'posted') {
          title = 'title';
          department = 'department';
          description = 'description';
          discipline = 'discipline';
          subject_area = 'subject_area';
          subject = 'subject';
        }
        else {
          title = disable_field('title');
          department = disable_field('department');
          description = disable_field('description');
          discipline = disable_field('discipline');
          subject_area =disable_field('subject_area');
          subject = disable_field('subject');
        }
        return [disable_field('code'), disable_field('state_calc_verbose'),
        title, department, description, discipline, subject_area, subject];
      }),
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: computed('role', 'starts_at', 'state', function() {
        let role = get(this, 'role');
        // admin user can edit all these fields
        if(role === 'helpdeskadmin') {
          return ['fek', 'fek_posted_at', 'starts_at', 'ends_at'];
        }
        // other users can edit date fields until the position become open
        else {
          let starts_at = this.get('model').get('starts_at'),
            before_open = moment().isBefore(starts_at),
            start_field, end_field;
          if(before_open) {
            start_field = 'starts_at';
            end_field = 'ends_at';
          }
          else {
            start_field = disable_field('starts_at');
            end_field = disable_field('starts_at')
          }
          return [disable_field('fek'), disable_field('fek_posted_at'), start_field, end_field];
        }
      }),
      layout: {
        flex: [50, 50, 50, 50]
      }
    },
    candidacies: {
      label: 'candidacy.menu_label',
      fields: [candidaciesField]
    },
    committee: {
      label: 'committee_members.label',
      fields: [
        committeeElectorsField('committee_internal', 'internal'),
        committeeElectorsField('committee_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_regular: {
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', 'internal'),
        committeeElectorsField('electors_regular_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_substitite: {
      label: 'electors_substitute_members.label',
      fields: [
        committeeElectorsField('electors_substitute_internal', 'internal'),
        committeeElectorsField('electors_substitute_external', 'external')
      ],
      layout: {
        flex: [100, 100]
      }
    }
  }
};

export {position};
