import {field} from 'ember-gen';
import {i18nField, get_registry_members} from 'ui/lib/common';
import {disable_field} from 'ui/utils/common/fields';
import moment from 'moment';
import {
  goToDetails, applyCandidacy, cancelPosition
} from 'ui/utils/common/actions';


const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

// params used for view details of candidacy from position view
const candidaciesField = function(type, hidden, calc, calc_params) {
  return field('candidacies', {
    valueQuery: function(store, params, model, value) {
      let position_id = model.get('id');
      // no use of params for now
      let query = {position: position_id};
      return store.query('candidacy', query);
    },
    label: null,
    modelMeta: {
      row: {
        fields: [
          'id',
          i18nField('candidate.full_name', {label: 'last_name.label'}),
          field('submitted_at_format', {label: 'submitted_at.label'}),
          field('updated_at_format', {label: 'updated_at.label'}),
          field('state_verbose', {label: 'candidacy.state'})
        ],
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails(type, hidden, calc, calc_params)
        },
      },
    },
    displayComponent: 'gen-display-field-table',
    disabled: true
  });
};

const managers_columns = [
  i18nField('last_name', {label: 'last_name.label'}),
  i18nField('first_name', {label: 'first_name.label'}),
  'role_verbose',
  field('email', {label: 'email.label'}),
  'mobile_phone_number'
];

const contactField = field('institution-managers', {
  label: null,
  modelName: 'institution-manager',
  modelMeta: {
    row: {
      fields: managers_columns,
    },
  },
  valueQuery: function(store, params, model, value) {
    // find department, to get get its institution
    return model.get('department')
      .then(function(department) {
        return  department.get('institution')
          .then(function(institution) {
            let institution_id = institution.get('id');
            /*
             * TODO: Check its functionality, what is going on with assistants
             *
             * get all managers of institution (assistants, institution manager,
             * substitute institution manager)
             */
            return store.query('institution-manager', {institution: institution_id})
              .then(function(managers) {
                let institution_manager = managers.filterBy('role', 'institutionmanager').get('firstObject'),
                  managers_ids = managers.getEach('id'),
                  // every institution has one sub_institution_manager
                  sub_institution_manager_id = `sub-${institution_id}`;
                /*
                 * The info of sub_institution_manager are on the model of
                 * institution manager. We extract them and create a
                 * institution-manager model with role sub_institution_manager.
                 * We do this because we want to display his info in a table.
                 */
                if(!store.hasRecordForId('institution-manager', sub_institution_manager_id)) {
                  let first_name = institution_manager.get('sub_first_name'),
                    last_name = institution_manager.get('sub_last_name'),
                    email = institution_manager.get('sub_email'),
                    mobile = institution_manager.get('sub_mobile_phone_number'),
                    sub;

                  sub = store.createRecord('institution-manager', {
                    role: 'sub_institution_manager',
                    id: sub_institution_manager_id,
                    first_name: first_name,
                    last_name: last_name,
                    email: email,
                    mobile_phone_number: mobile
                  });
                }
                if(!managers_ids.includes(sub_institution_manager_id)) {
                  managers_ids.push(sub_institution_manager_id);
                }

                /*
                 * We have all the managers of the institution in store.
                 * In the position details we display a table field with the
                 * contact info of:
                 * - institution manager (position's institution)
                 * - substitute manager (position's institution)
                 */
                return store.peekAll('institution-manager').filter(function(manager) {
                  let role = manager.get('role'),
                    id = manager.get('id'),
                    is_institution_manager = (role === 'institutionmanager' && managers_ids.includes(id)),
                    is_sub_institution_manager = (role === 'sub_institution_manager' && managers_ids.includes(id));
                  return (is_institution_manager || is_sub_institution_manager);
                });
              });
          });
      });
  },
  displayComponent: 'gen-display-field-table'

});

/*
 * These fields can get a value from the members of a registry.
 * The table with the members data have the same form
 */
function committeeElectorsField(field_name, registry_type) {
  let label = `registry.type.${registry_type}`;

  return field(field_name, {
    label: label,
    disabled: computed('model.changeset.committee_set_file', 'model.changeset.electors_set_file', function(){
      let file1 = get(this, 'model.changeset.committee_set_file');
      let file2 = get(this, 'model.changeset.electors_set_file');
      if(field_name.startsWith('committee')) {
        return !(file1 && file1.content);
      } else {
        return !(file2 && file2.content);
      }
    }),
    query: computed('position', function() {
      return function(table, store, field, params) {
        let departmentID = table.get("form.changeset.department.id");
        return store.query('registry', {department: departmentID}).then(function (registries) {
          /*
           * There are max 2 registries per department
           * Here we take the external (type 2) registry
           */
          let registry = registries.findBy('type', registry_type);
          return get_registry_members(registry, store, params);
        });
      };
    }),
    modelMeta: {
      row: {
        fields: computed('', function() {
          // all electors tables have ena extra column
          if(field_name.startsWith('electors')) {
            return ['id',
              i18nField('last_name', {label: 'last_name.label'}),
              i18nField('first_name', {label: 'first_name.label'}),
              i18nField('department.title', {label: 'department.label'}),
              i18nField('department.institution.title'),
              'is_foreign_descr',
              field('email', {label: 'email.label'}),
              'active_elections'
            ];
          }
          else {
            return ['id',
              i18nField('last_name', {label: 'last_name.label'}),
              i18nField('first_name', {label: 'first_name.label'}),
              i18nField('department.title', {label: 'department.label'}),
              i18nField('department.institution.title'),
              'is_foreign_descr',
              field('email', {label: 'email.label'}),
            ];
          }
        }),
        actions: ['goToDetails'],
        actionsMap: {
          goToDetails: goToDetails(undefined, false, false)
        }
      },
    },
    displayComponent: 'gen-display-field-table'

  });
};

const historyField = field('past_positions', {
  valueQuery: function(store, params, model, value) {
    let id = model.get('id');
    let query = {id: id, history: true};
    return store.query('position', query);
  },
  label: null,
  modelMeta: {
    row: {
      fields: ['id', 'code', 'state_calc_verbose',
        field('updated_at_format', {label: 'updated_at.label'})
      ],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: goToDetails(undefined, false, false)
      }
    },
  },
  displayComponent: 'gen-display-field-table'
});

export {
  contactField, candidaciesField, committeeElectorsField,
  historyField
};
