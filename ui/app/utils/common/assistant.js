import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';
import {i18nField} from 'ui/lib/common';

const {
  assign,
  computed,
  get,
  set,
  computed: { or }
} = Ember;

// Fieldsets for assistants profile

const FIELDSET = {
  label: 'fieldsets.labels.user_info',
  text: 'fieldsets.text.assistant_profile',
  fields: [
    disable_field('user_id'),
    disable_field('username'),
    disable_field('email'),
    'mobile_phone_number',
    'home_phone_number',
    disable_field('first_name'),
    disable_field('last_name'),
    disable_field('father_name'),
    disable_field('id_passport'),
  ],
  layout: {
    flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
  }
};

const FIELDSET_PERMISSIONS_INFO = {
  label: 'fieldsets.labels.more_info',
  fields: [
    field('institution', {displayAttr: 'title_current', disabled: true}),
    field('is_secretary_verbose', { disabled: true, label: 'is_secretary.label' }),
    disable_field('can_create_positions_verbose'),
    disable_field('can_create_registries_verbose'),
    field('departments', {
      disabled: true,
      label: 'department.menu_label',
      modelName: 'department',
      modelMeta: {
        row: {
          fields: [i18nField('title', { label: 'title.label' })],
          actionsMap: { remove: { hidden: true } }
        }
      },
      displayComponent: 'gen-display-field-table'
    })
  ],
  layout: {
    flex: [100, 33, 33, 33, 100]
  }
};

const FIELDSET_DETAILS = {
  label: 'fieldsets.labels.user_info',
  fields: [
    'user_id',
    'username',
    'email',
    'mobile_phone_number',
    'home_phone_number',
    'first_name_current',
    'last_name_current',
    'father_name_current',
    'id_passport',
    field('institution', {displayAttr: 'title_current'}),
    'is_secretary_verbose',
    'can_create_positions_verbose',
    'can_create_registries_verbose',
  ],
  layout: {
        flex: [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 33, 33, 33]
  }
}

export {
  FIELDSET,
  FIELDSET_DETAILS,
  FIELDSET_PERMISSIONS_INFO
}
