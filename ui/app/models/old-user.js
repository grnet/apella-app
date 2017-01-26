import DS from 'ember-data';
import ENV from 'ui/config/environment';

const { computed, get } = Ember;


export default DS.Model.extend({
  user_id: DS.attr(),
  username: DS.attr(),
  shibboleth_id: DS.attr(),
  role: DS.attr(),
  name_el: DS.attr(),
  surname_el: DS.attr(),
  fathername_el: DS.attr(),
  name_en: DS.attr(),
  surname_en: DS.attr(),
  fathername_en: DS.attr(),
  email: DS.attr(),
  mobile: DS.attr({label: 'mobile_phone_number.label'}),
  phone: DS.attr({label: 'home_phone_number.label'}),
  person_id_number: DS.attr({label: 'id_passport.label'}),
  is_foreign: DS.attr(),
  speaks_greek: DS.attr(),
  professor_subject_id: DS.attr(),
  professor_rank: DS.attr({label: 'rank.label'}),
  professor_institution_id: DS.attr(),
  professor_institution_freetext: DS.attr({label: 'institution_freetext.label'}),
  professor_department_id: DS.attr(),
  professor_appointment_gazette_url: DS.attr({label: 'fek.label'}),
  professor_subject_from_appointment: DS.attr(),
  professor_subject_optional_freetext: DS.attr(),
  professor_institution_cv_url: DS.attr({label: 'cv_url.label'}),
  manager_institution_id: DS.attr(),
  manager_appointer_authority: DS.attr({label: 'manager.label.authority_type'}),
  manager_appointer_fullname: DS.attr({label: 'manager.label.authority_full_name'}),
  manager_deputy_name_el: DS.attr({label: 'name_el.label'}),
  manager_deputy_surname_el: DS.attr({label: 'surname_el.label'}),
  manager_deputy_fathername_el: DS.attr({label: 'fathername_el.label'}),
  manager_deputy_name_en: DS.attr({label: 'name_en.label'}),
  manager_deputy_surname_en: DS.attr({label: 'surname_en.label'}),
  manager_deputy_fathername_en: DS.attr({label: 'fathername_en.label'}),
  manager_deputy_mobile: DS.attr({label: 'mobile_phone_number.label'}),
  manager_deputy_phone: DS.attr({label: 'home_phone_number.label'}),
  manager_deputy_email: DS.attr({label: 'email.label'}),
  role_status: DS.attr({label: 'state.label'}),

  speaks_greek_verbose: computed('speaks_greek', function(){
    let f = get(this, 'speaks_greek');
    if (f == 'f') return '-';
    if (f == 't') return '✓';
    return '-';
  }),
  is_foreign_verbose: computed('is_foreign', function(){
    let f = get(this, 'is_foreign');
    if (f == 'f') return '-';
    if (f == 't') return '✓';
    return '-';
  })
});

