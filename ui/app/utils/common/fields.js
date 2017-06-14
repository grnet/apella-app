import {field} from 'ember-gen';

let {
  computed, get
} = Ember;



function disable_field(el) {
  return field(el, {
      disabled: true
  })
}

function departmentInstitutionFilterField(dataKey='department') {
  return field(
    'department',
    {
      autocomplete: true,
      label: 'department.label',
      type: 'model',
      displayAttr: 'title_current',
      modelName: 'department',
      disabled: computed('model.changeset.institution.id', function() {
        return !this.get('model.changeset.institution');
      }),
      dataKey: dataKey,
      query: computed('model.changeset.institution.id', function() {
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
}

export {disable_field, departmentInstitutionFilterField}
