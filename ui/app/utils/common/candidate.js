import Ember from 'ember';
import validate from 'ember-gen/validate';
import {fileField} from 'ui/lib/common';

const {
  computed: { or }
} = Ember;

const FILES_FIELDS = [
  fileField('id_passport_file', 'candidate', 'id_passport', {
    readonly: true
  }, { replace: true }),
  fileField('cv', 'candidate', 'cv', {
    readonly: true
  }, { replace: true }),
  fileField('diplomas', 'candidate', 'diploma', {
    readonly: true
  }, {
    multiple: true
  }),
  fileField('publications', 'candidate', 'publication', {
    readonly: true
  }, {
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
