import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';

const { computed } = Ember;

export default ApellaGen.extend({
  modelName: 'old-user',
  path: 'old-users',
  order: 750,
  auth: true,
  list: {
    page: {
      title: 'old_user.menu_label',
    },
    menu: {
      label: 'old_user.menu_label',
      icon: 'wc',
    },
    layout: 'table',
    row: {
      fields: ['user_id', 'username', 'name_el', 'surname_el', 'email', 'role', 'role_status'],
      actions: ['gen:details'],
    },
    filter: {
      active: false,
      serverSide: true,
      search: true,
      searchFields: ['user_id', 'username', 'email', 'surname_el', 'shibboleth_id', 'surname_en', 'role', 'role_status']
    },
    sort: {
      active: true,
      serverSide: true,
      fields: ['user_id', 'username', 'email', 'surname_el', 'role', 'role_status']
    },
  },
  details: {
    page: {
      title: computed.readOnly('model.username')
    },
    fieldsets: [{
      label: 'fieldsets.labels.user_info',
      fields: ['user_id', 'username', 'role', 'name_el', 'name_en', 'surname_el', 'surname_en', 'fathername_el', 'fathername_en', 'email', 'mobile', 'phone'],
      layout: {
        flex: [50, 25, 25, 50, 50, 50, 50, 50, 50, 50, 25, 25]
      }
    }, {
      label: 'fieldsets.labels.professor_profile',
      fields: ['shibboleth_id', 'person_id_number', 'is_foreign_verbose', 'speaks_greek_verbose', 'professor_subject_id', 'professor_rank', 'professor_institution_id','professor_department_id',  'professor_institution_freetext', 'professor_appointment_gazette_url', 'professor_subject_from_appointment', 'professor_subject_optional_freetext', 'professor_institution_cv_url', 'role_status'],
      layout: {
        flex: [25, 25, 25, 25, 25, 25, 25, 25, 50, 50, 50, 50, 50, 50]
      }
    }, {
      label: 'fieldsets.labels.manager_info',
      fields: [
        'manager_appointer_authority', 'manager_appointer_fullname', 'manager_institution_id'],
      layout: {
        flex: [25, 25, 50]
      }
    }, {
      label: 'fieldsets.labels.sub_info',
      fields: [
        'manager_deputy_name_el', 'manager_deputy_surname_el',
        'manager_deputy_fathername_el', 'manager_deputy_name_en',
        'manager_deputy_surname_en', 'manager_deputy_fathername_en',
        'manager_deputy_mobile', 'manager_deputy_phone', 'manager_deputy_email',],
      layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 25]
      }


    }]
  }
});
