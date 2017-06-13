import {field} from 'ember-gen';

let {
  computed, get
} = Ember;



function disable_field(el) {
  return field(el, {
      disabled: true
  })
}

let departmentInstitutionFilterField =  field(
  'department',
  {
    autocomplete: true,
    label: 'department.label',
    type: 'model',
    displayAttr: 'title_current',
    modelName: 'department',
    disabled: computed('model.changeset.institution', function() {
      return !this.get('model.changeset.institution');
    }),
    dataKey: 'department',
    query: computed('model.changeset.institution', function() {
      let inst = this.get('model.changeset.institution.id');
      return function(select, store, field, params) {
        let locale = select.get('i18n.locale');
        params = params || {};
        params.ordering = `title_${locale}`;
        params.institution = inst;
        return store.query('department', params);
      }
    })
  }
);


export {disable_field, departmentInstitutionFilterField}
