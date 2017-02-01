import Ember from 'ember';
import validate from 'ember-gen/validate';
import {i18nValidate} from 'ui/validators/i18n';
import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';

const {
  assign,
  computed,
  get,
  set,
  computed: { or }
} = Ember;


const FILES_FIELDSET = {
  label: 'fieldsets.labels.candidate_files',
  fields: [
    fileField('cv', 'professor', 'cv', {
    }, {
      replace: true
    }),
    fileField('diplomas', 'professor', 'diploma', {}, {
      multiple: true
    }),
    fileField('publications', 'professor', 'publication', {}, {
      multiple: true
    }),
  ],
  layout: {
    flex: [100, 100, 100]
  }
};


const FIELDS = computed('model.is_foreign', 'model.changeset.cv_in_url', function(){
  let f = [
    'rank',
    'discipline_text',
    field('cv_in_url', {
      hint: 'cv_in_url.hint',
    }),
    field('cv_url', {
      hint: 'cv_url.hint',
      disabled: computed('model.changeset.cv_in_url', function() {
        let check = get(this, 'model.changeset.cv_in_url');
        if (!check) { Ember.run.once(this, () => set(this, 'model.changeset.cv_url', '')) };
        return !check;
      })
    }),
    fileField('cv_professor', 'professor', 'cv_professor', {
      readonly: or('user.is_verified', 'user.verification_pending'),
      disabled: computed('model.changeset.cv_in_url', function() {
        let check = get(this, 'model.changeset.cv_in_url');
        if (check) {
          Ember.run.once(this, () =>
            set(this, 'model.changeset.cv_professor', null)
          ) };
        return check;
      })
    }, {
      replace: true
    }),

  ];

  let f_domestic = [
    field('institution', {displayAttr: 'title_current'}),
    field('department', {displayAttr: 'title_current'}),
    field('discipline_in_fek',{
      hint: 'discipline_in_fek.hint',
    }),
    'fek',
  ];

  let f_foreign = [
    'institution_freetext',
    'speaks_greek',
  ];

  if (get(this, 'model.is_foreign')) {
    return f.concat(f_foreign);
  } else {
    return f.concat(f_domestic);
  }

});

const FIELDS_REGISTER = FIELDS;

const FIELDS_REGISTER_REQUIRED = computed('model.is_foreign', function(){
  if (get(this, 'model.is_foreign')) {
    return ['institution_freetext'];
  } else {
    return ['institution', 'department', 'rank', 'fek'];
  }
});

const FLEX = computed('model.is_foreign', function() {
  if (get(this, 'model.is_foreign') ) {
    return [50, 50, 50, 50, 100]
  } else {
    return [50, 50, 50, 50, 100, 50, 50, 100, 100]
  }
})

const FIELDSET = {
  label: 'fieldsets.labels.professor_profile',
  fields: FIELDS,
  layout: {
    flex: FLEX
   }
}

const FIELDSET_REGISTER = Ember.assign({}, FIELDSET, {
  label: Ember.computed('model.is_academic', function() {
    let academic = this.get('model.is_academic');
    if (academic) { return 'fieldsets.labels.user_info.academic'; }
    return 'fieldsets.labels.more_info';
  }),
  required: FIELDS_REGISTER_REQUIRED,
  fields: FIELDS_REGISTER
});

const VALIDATORS = {
  cv_url: [validate.format({allowBlank: true, type:'url'})],
  institution: [validate.presence(true)],
}


export {
  FILES_FIELDSET,
  FIELDSET,
  FIELDSET_REGISTER,
  VALIDATORS
}