import { field } from 'ember-gen';
import { i18nField, fileField } from 'ui/lib/common';

const { get } = Ember;

// Fieldsets for quickDetailsView of professors
let fs_user = {
  label: 'user_data',
  fields: [
    'user_id',
    'old_user_id',
    i18nField('full_name'),
    i18nField('father_name', {label: 'father_name.label'}),
  ],
  layout: {
    flex: [50, 50, 50, 50]
  }
};

let fs_contact = {
  label: 'contact',
  fields: [
    'email',
    'home_phone_number',
    'mobile_phone_number'
  ],
  layout: {
    flex: [100, 50, 50]
  }
};

let fs_prof_domestic = {
  label: 'professor_profile',
  fields: [
    'is_foreign_descr',
    field('institution_global', {label: 'institution.label'}),
    i18nField('department.title', {label: 'department.label'}),
    'discipline_text',
    'rank',
    'cv_url',
    fileField('cv_professor', 'professor', 'cv_professor',
      { readonly: true, label: 'cv.label' }),
    'fek',
    field('discipline_in_fek_verbose', { label: 'discipline_in_fek.label' })
  ],
  layout: {
    flex: [50, 50, 50, 50, 100, 100, 100, 50, 50]
  }
};

let fs_prof_foreign = {
  label: 'professor_profile',
  fields: [
    'is_foreign_descr',
    field('institution_global', {label: 'institution.label'}),
    'discipline_text',
    'rank',
    'cv_url',
    fileField('cv_professor', 'professor', 'cv_professor',
      { readonly: true, label: 'cv.label' }),
    field('speaks_greek_verbose', {label: 'speaks_greek.label'}),
  ],
  layout: {
    flex: [50, 50, 50, 50, 100, 100, 50]
  }
};

let fs_prof_leave = {
  label: 'fieldsets.labels.leave',
  fields: [
    'leave_starts_at_format',
    'leave_ends_at_format',
    'on_leave_verbose',
    fileField('leave_file', 'professor', 'leave_file', {
      readonly: true,
    }),
  ],
  layout: {
    flex: [50, 25, 25, 100]
  }
};


function peak_fs_professors() {
  let professor = get(this, 'model'),
    is_foreign = professor.get('is_foreign'),
    head = [fs_user, fs_contact];
  if(is_foreign) {
    return head.concat(fs_prof_foreign);
  }
  else {
    let res =  head.concat(fs_prof_domestic);
    let on_leave = get(this, 'model.on_leave');
    if (on_leave) {
      res = res.concat(fs_prof_leave);
    }
    return res;
  }
};

export { fs_user,  fs_contact, fs_prof_domestic, fs_prof_foreign, peak_fs_professors };
