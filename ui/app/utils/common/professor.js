import Ember from 'ember';
import ENV from 'ui/config/environment';
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
  computed: { or, bool, not }
} = Ember;


const FILES_FIELDSET = {
  label: 'fieldsets.labels.candidate_files',
  text: computed('model.is_verified', function(){
    if (get(this, 'model.is_verified')) {
      return 'fieldsets.text.candidate_profile'
    }
    return ''
  }),
  fields: [
    fileField('cv', 'professor', 'cv', {
      readonly: computed('role', function() {
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
      replace: true
    }),
    fileField('diplomas', 'professor', 'diploma', {
      readonly: computed('role', function() {
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
    fileField('publications', 'professor', 'publication', {
      readonly: computed('role', function() {
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
  ],
  layout: {
    flex: [100, 100, 100]
  }
};


const FIELDS = computed('model.is_foreign', function(){
  let f = [
    'rank',
    'discipline_text',
    field('cv_in_url', {
      hint: 'cv_in_url.hint',
    }),
    field('cv_url', {
      hint: 'cv_url.hint',
      required: bool('model.changeset.cv_in_url'),
      disabled: computed('model.changeset.cv_in_url', function() {
        let check = get(this, 'model.changeset.cv_in_url');
        if (!check) { Ember.run.once(this, () => set(this, 'model.changeset.cv_url', '')) };
        if (check) { get(this, 'model.changeset').propertyDidChange('cv_professor'); }
        return !check;
      })
    }),
    fileField('cv_professor', 'professor', 'cv_professor', {
      readonly: computed('role', 'user.is_verified', 'user.verification_pending', function() {
        let user_role = get(this, 'role'),
          forbid_edit_roles = ['ministry'],
          is_verified = get(this, 'user.is_verified'),
          verification_pending = get(this, 'user.verification_pending');
        if(forbid_edit_roles.indexOf(user_role) > -1 || is_verified || verification_pending) {
          return true;
        }
        else {
          return false;
        }
      }),
      required: not('model.changeset.cv_in_url'),
      disabled: computed('model.changeset.cv_in_url', function() {
        let check = get(this, 'model.changeset.cv_in_url');
        let changed = get(this, 'model.cv_in_url') != check;
        let cv = get(this, 'model.cv_professor');
        if (!changed) { return; }

        let prompt =  this.container.lookup("service:prompt");
        if (check && cv && cv.content) { Ember.run.once(this, () => {
          prompt.prompt({
            title: 'confirm.cv.professor.unset.title',
            message: 'confirm.cv.professor.unset.message'
          }).then(() => {
            let file = get(this, 'model.cv_professor');
            file && file.content && file.content.destroyRecord().then(() => {
              Ember.run.once(this, () => {
                get(this, 'model').set('cv_professor', null);
                get(this, 'model.changeset').set('cv_professor', null);
              });
            });
          }).catch(() => {
            Ember.run.once(this, () => {
              get(this, 'model').set('cv_in_url', false);
              get(this, 'model.changeset').set('cv_in_url', false);
              get(this, 'model.changeset').set('cv_url', null);
            });
          });
        }) };
        return check;
      })
    }, {
      replace: true
    }),

  ];

  let f_domestic = [
    field('institution', {
      query: computed('user.shibboleth_idp', function() {
        let idp = get(this, 'user.shibboleth_idp');
        return function(table, store, field, params) {
          var model = get(field, 'modelName');
          params = params || {};
          if (idp && idp.length > 0 && (ENV.APP.idp_whitelist || []).indexOf(idp) === -1) { params.idp = idp; }
          if (params) {
            return store.query(model, params);
          }
          return store.findAll(model);
        }
      }),
      displayAttr: 'title_current'
    }),
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
    return [50, 50, 50, 50, 100, 50, 50]
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

const LEAVE_FIELDSET_DETAILS = {
  label: 'fieldsets.labels.leave',
  text: 'fieldsets.text.leave',
  fields: [
    'on_leave_verbose',
    'leave_starts_at_format',
    'leave_ends_at_format',
    fileField('leave_file', 'professor', 'leave_file', {
      readonly: true,
    }),
  ],
  layout: {
    flex: [50, 25, 25, 100]
  }
}




const VALIDATORS = {
  cv_url: [validate.format({allowBlank: true, type:'url'})],
  institution: [validate.presence(true)],
}


export {
  FILES_FIELDSET,
  FIELDSET,
  FIELDSET_REGISTER,
  VALIDATORS,
  LEAVE_FIELDSET_DETAILS,
}
