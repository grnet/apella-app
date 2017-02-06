import Ember from 'ember';
import validate from 'ember-gen/validate';
import {fileField} from 'ui/lib/common';

const {
  computed: { or }
} = Ember;

const FILES_FIELDS = [
  fileField('id_passport_file', 'candidate', 'id_passport', {
    readonly: or('model.is_verified', 'model.verification_pending')
  }, { replace: true }),
  fileField('cv', 'candidate', 'cv', {
  }, { replace: true }),
  fileField('diplomas', 'candidate', 'diploma', {}, {
    multiple: true
  }),
  fileField('publications', 'candidate', 'publication', {}, {
    multiple: true
  }),
]

const FILES_FIELDSET = {
  label: 'fieldsets.labels.candidate_profile',
  fields: FILES_FIELDS,
  layout: {
    flex: [100, 100, 100, 100]
  }
}
export {
  FILES_FIELDSET
}
