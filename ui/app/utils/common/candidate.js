import Ember from 'ember';
import validate from 'ember-gen/validate';
import {fileField} from 'ui/lib/common';

const {
  get,
  computed,
  computed: { or }
} = Ember;

const FILES_FIELDS = [
  fileField('id_passport_file', 'candidate', 'id_passport', {
    readonly: computed('role', 'model.is_verified', 'model.verification_pending', function() {
      // NOTE: When the candidate is in his profile the role is undefined
      let user_role = get(this, 'role'),
        forbid_edit_roles = ['helpdeskuser', 'ministry'];
      if(forbid_edit_roles.indexOf(user_role) > -1) {
        return true;
      }
      else {
        return get(this, 'model.is_verified') || get(this, 'model.verification_pending');
      }
    })
  }, { replace: true }),
  fileField('cv', 'candidate', 'cv', {
    readonly: computed('role', function() {
      // NOTE: When the candidate is in his profile the role is undefined
      let user_role = get(this, 'role'),
        forbid_edit_roles = ['helpdeskuser', 'ministry'];
      if(forbid_edit_roles.indexOf(user_role) > -1) {
        return true;
      }
      else {
        return false;
      }
    })
  }, { replace: true }),
  fileField('diplomas', 'candidate', 'diploma', {
    readonly: computed('role', function() {
      // NOTE: When the candidate is in his profile the role is undefined
      let user_role = get(this, 'role'),
        forbid_edit_roles = ['helpdeskuser', 'ministry'];
      if(forbid_edit_roles.indexOf(user_role) > -1) {
        return true;
      }
      else {
        return false;
      }
    })
  }, {
    multiple: true
  }),
  fileField('publications', 'candidate', 'publication', {
    readonly: computed('role', function() {
      // NOTE: When the candidate is in his profile the role is undefined
      let user_role = get(this, 'role'),
        forbid_edit_roles = ['helpdeskuser', 'ministry'];
      if(forbid_edit_roles.indexOf(user_role) > -1) {
        return true;
      }
      else {
        return false;
      }
    })
  }, {
    multiple: true
  }),
]

const FILES_FIELDSET = {
  label: 'fieldsets.labels.candidate_profile',
  text: computed('model.is_verified', function(){
    if (get(this, 'model.is_verified')) {
      return 'fieldsets.text.candidate_profile'
    }
    return ''
  }),
  fields: FILES_FIELDS,
  layout: {
    flex: [100, 100, 100, 100]
  }
}
export {
  FILES_FIELDSET
}
