import _ from 'lodash/lodash';
import {field} from 'ember-gen';
import {disable_field, i18nField} from 'ui/utils/common/fields';
import {fileField} from 'ui/lib/common';
import {getFile} from 'ui/utils/files';
import moment from 'moment';
import {
  candidaciesField, committeeElectorsField, historyField,
  contactField
} from 'ui/lib/position/table_fields';

const {
  computed,
  computed: { reads, or, bool, not, and },
  get,
  set,
  merge, assign
} = Ember;

const  position = {
  create: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: ['title',
        field('department', {
          autocomplete: true,
          query: function(table, store, field, params) {

            // If the logged in user is an assistant, department field is a
            // select list  with the assistant's departments
            let role = get(field, 'session.session.authenticated.role');
            if (role == 'assistant') {
              let deps = get(field, 'session.session.authenticated.departments');
              let promises = deps.map((url) => {
                let id = url.split('/').slice(-2)[0];
                return store.findRecord('department', id);
              })

              var promise = Ember.RSVP.all(promises).then((res) => {
                return res;
              }, (error) => {
                return [];
              });

              return DS.PromiseArray.create({
                promise : promise
              })
            }

            // on load sort by title
            let locale = get(table, 'i18n.locale');
            let ordering_param = {
              ordering: `title__${locale}`
            };
            let query;
            // If the logged in user is an institutionmanager, department field
            // is a select list with all the deparments that belong to the
            // institutionmanager's institution
            if (role == 'institutionmanager') {
              let user_institution = get(field, 'session.session.authenticated.institution');
              let id = user_institution.split('/').slice(-2)[0];
              query = assign({}, { institution: id }, ordering_param);
            } else {
              query = ordering_param;
            }
            return store.query('department', query);
          }
        }),
        'description',
        'discipline',
        'subject_area',
        'subject'
      ],
      layout: {
        flex: [50, 50, 100, 100, 50, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: ['fek', 'fek_posted_at', 'starts_at', 'ends_at'],
      layout: {
        flex: [50, 50, 50, 50]
      },
    }
  },
  details: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: ['code', 'old_code', 'state_calc_verbose', 'title',
        field('department.title_current', {label: 'department.label'}),
        'department.institution.title_current',
        'discipline', 'description', field('subject_area.title_current',{label: 'subject_area.label'}),
        field('subject.title_current', {label: 'subject.label'})],
      layout: {
        flex: [25, 25, 50, 50, 50, 50, 50, 100, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: ['fek', field('fek_posted_at_format', {label: 'fek_posted_at.label'}),
        field('starts_at_format', {label: 'starts_at.label'}),
        field('ends_at_format', {label: 'ends_at.label'})],
      layout: {
        flex: [50, 50, 50, 50]
      }
    },
    candidacies: {
      label: 'candidacy.menu_label',
      fields: computed('user.role','user.user_id', 'user.id', 'model.electors',
        'model.committee', 'model.can_apply', function() {
        let user = get(this, 'user'),
          user_id = get(user, 'user_id'),
          role = get(user, 'role'),
          position = get(this, 'model'),
          type = 'candidacy',
          hidden = false,
          calculate = false,
          is_position_candidate = false,
          store = get(position, 'store');
        /*
         * Helpdesk user and admin should see candidacies' details.
         * If an assistant or a manager is allowed to see a position should see
         * and candidacies' details.
         */
        if (['helpdeskadmin','helpdeskuser','institutionmanager', 'assistant'].indexOf(role) > -1) {
          hidden = false;
          calculate = false;
        }
        /*
         * A professor can see candidacies' details when:
         * - Is member in any related committee of the position
         * - The candidacy is his/hers
         * - The candidacy has othersCanView true and the professor is also
         *   candidate for this position.
         *
         * The last 2 are calculated inside candidaciesField.
         *
         * A candidate can see candidacies' details when:
         * - The candidacy is his/hers
         * - The candidacy has othersCanView true and the candidate has also
         *   sublmit candidacy for this position.
         *
         * These 2 are calculated inside candidaciesField.
         */

        else if (['professor', 'candidate'].indexOf(role) > -1) {
          /*
           * can_apply attribute is true when a professor/candidate hasn't
           * applied candidacy for the position.
           *
           * Here we use this property to check if the logged in user is a
           * candidate of the position.
           */
          let position_candidates = [];
          store.peekAll('candidacy').forEach(function(candidacy) {
            let candidacy_pos_id = candidacy.belongsTo('position').link().split('/').slice(-2)[0],
              candidate_id = candidacy.belongsTo('candidate').link().split('/').slice(-2)[0];
            if(candidacy_pos_id === position.id) {
              position_candidates.push(candidate_id);
            }
          });

          if(position_candidates.indexOf(user_id) > -1) {
            is_position_candidate = true;
          }
          if (role === 'professor') {
            // TODO: improve foreign professors
            let user_department = get(user, 'department') || "",
              user_department_id = user_department.split('/').slice(-2)[0],
              position_department_id = position.belongsTo('department').link().split('/').slice(-2)[0];
            if(user_department_id === position_department_id) {
              hidden = false;
              calculate = false;
            }
            else {
              let electors = position.hasMany('electors').ids(),
                committee = position.hasMany('committee').ids(),
                related_profs = _.union(electors, committee),
                professor_id = user.id,
                is_related_prof = related_profs.indexOf(professor_id) > -1;
              if(is_related_prof) {
                hidden = false;
                calculate = false;
              }
              else {
                hidden = undefined;
                calculate = true;
              }
            }
          }
          else if (role === 'candidate') {
            hidden = undefined;
            calculate = true;
          }
        }
        return [candidaciesField(type, hidden, calculate, is_position_candidate)]
      })
    },
    committee: {
      label: 'fieldsets.labels.committee',
      fields: [
        fileField('committee_set_file', 'position', 'committee_set_file', {
          readonly: true
        }),
        committeeElectorsField('committee_internal', 'internal', false, false),
        committeeElectorsField('committee_external', 'external', false, false),
        fileField('committee_proposal', 'position', 'committee_proposal', {
          readonly: true
        }),
        fileField('committee_note', 'position', 'committee_note', {
          readonly: true
        }),
      ],
      layout: {
        flex: [100, 100, 100, 100, 100]
      }
    },
    electors: {
      label: 'fieldsets.labels.electors',
      fields: [
        fileField('electors_set_file', 'position', 'electors_set_file', {
          readonly: true
        }),
        field('electors_meeting_to_set_committee_date_format', {
          label: 'electors_meeting_to_set_committee_date.label'
        }),
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_regular: {
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', 'internal', false, false),
        committeeElectorsField('electors_regular_external', 'external', false, false)
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_substitite: {
      label: 'electors_sub_members.label',
      fields: [
        committeeElectorsField('electors_sub_internal', 'internal', false, false),
        committeeElectorsField('electors_sub_external', 'external', false, false)
      ],
      layout: {
        flex: [100, 100]
      }
    },
    election: {
      label: 'fieldsets.labels.election',
      fields: [
        fileField('electors_meeting_proposal', 'position', 'electors_meeting_proposal', {
          readonly: true,
        }),
        'electors_meeting_date_format',
        fileField('nomination_proceedings', 'position', 'nomination_proceedings', {
          readonly: true,
        }),
        fileField('proceedings_cover_letter', 'position', 'proceedings_cover_letter', {
          readonly: true,
        }),
        field('elected.full_name_current', {label: 'elected.full_name.label'}),
        field('second_best.full_name_current', {label: 'second_best.full_name.label'}),
        fileField('nomination_act', 'position', 'nomination_act', {
          readonly: true,
        }),
        'nomination_act_fek',
        fileField('revocation_decision', 'position', 'revocation_decision', {
          readonly: true
        }),
        fileField('failed_election_decision', 'position', 'failed_election_decision', {
          readonly: true
        }),
      ],
      layout: {
        flex: [100, 100, 100, 100, 50, 50, 100, 100, 100, 100]
      }
    },

    assistant_files: {
      label: 'fieldsets.labels.assistant_files',
      fields: [
        fileField('assistant_files', 'position', 'assistant_files', {
          readonly: true
        }, {
          multiple: true
        }),
      ]
    },
    history: {
        label: 'position.history.title',
        fields: computed('model.id', function() {
          let position_id = get(this, 'model.id')
          return [historyField(position_id)];
        })
      },
    contact: {
      label: 'contact',
      fields: [contactField]
    }
  },
  edit: {
    basic: {
      label: 'fieldsets.labels.basic_info',
      fields: computed('role', 'state', function() {
        /*
         * For posted positions:
         * - When they are open or closed helpdeskuser and heldeskadmin can
         *   edit these fields.
         * - Before they open assistant and manager can edit most of the fields
         *
         * In all the other states the fields of this fieldset are disabled.
         */

        let role = get(this, 'role'),
          state = get(this, 'model.state'),
          is_open = get(this, 'model.is_open'),
          is_closed = get(this, 'model.is_closed'),
          before_open = (!(is_open || is_closed) && (state === 'posted')),
          title, department, description, discipline, subject_area, subject,
          disable_fields = true,
          institution_roles = ['institutionmanager', 'assistant'],
          helpdesk_roles = ['helpdeskadmin', 'helpdeskuser'];

        if(state === 'posted') {
          if(helpdesk_roles.indexOf(role) > -1) {
            disable_fields = false;
          }
          else if((institution_roles.indexOf(role) > -1) && before_open) {
            disable_fields = false;
          }
        }
        if(disable_fields) {
          title = disable_field('title');
          department = disable_field('department');
          description = disable_field('description');
          discipline = disable_field('discipline');
          subject_area =disable_field('subject_area');
          subject = disable_field('subject');
        }
        else {
          title = 'title';
          department = field('department', {
            autocomplete: true,
            required: true,
            query: function(select, store, field, params) {

              // If the logged in user is an assistant, department field is a
              // select list  with the assistant's departments
              let role = get(field, 'session.session.authenticated.role');
              if (role == 'assistant') {
                let deps = get(field, 'session.session.authenticated.departments');
                let promises = deps.map((url) => {
                  let id = url.split('/').slice(-2)[0];
                  return store.findRecord('department', id);
                });

                var promise = Ember.RSVP.all(promises).then((res) => {
                  return res;
                }, (error) => {
                  return [];
                });

                return DS.PromiseArray.create({
                  promise : promise
                });
              }

              // on load sort by title
              let locale = get(select, 'i18n.locale');
              let ordering_param = {
                ordering: `title__${locale}`
              };
              let query;
              // If the logged in user is an institutionmanager, department field
              // is a select list with all the deparments that belong to the
              // institutionmanager's institution
              if (role == 'institutionmanager') {
                let user_institution = get(field, 'session.session.authenticated.institution');
                let id = user_institution.split('/').slice(-2)[0];
                query = assign({}, { institution: id }, ordering_param);
              }
              else {
                // TODO: Get only the deparments of the institution of the
                // position
                query = ordering_param;
              }
              return store.query('department', query);
            }
          });
          description = 'description';
          discipline = 'discipline';
          subject_area = 'subject_area';
          subject = 'subject';
        }
        return [disable_field('code'), disable_field('old_code'), disable_field('state_calc_verbose'),
        department, title, description, discipline, subject_area, subject];
      }),
      layout: {
        flex: [50, 50, 50, 50, 100, 100, 100, 50, 50]
      }
    },
    details: {
      label: 'fieldsets.labels.details',
      fields: computed('role', 'is_open', 'is_closed', 'state', function() {
        /*
         * For posted positions:
         * - When they are open or closed, helpdeskuser and heldeskadmin can
         *   edit these fields.
         * - Before they open assistant and manager can edit most of the fields
         *
         * In all the other states the fields of this fieldset are disabled.
         */

        let role = get(this, 'role'),
          state = get(this, 'model.state'),
          is_open = get(this, 'model.is_open'),
          is_closed = get(this, 'model.is_closed'),
          disable_fields = true,
          institution_roles = ['institutionmanager', 'assistant'],
          helpdesk_roles = ['helpdeskadmin', 'helpdeskuser'],
          fek, fek_posted_at, starts_at, ends_at;

        if(state === 'posted') {
          if(is_open || is_closed) {
            if(helpdesk_roles.indexOf(role) > -1) {
              disable_fields = false;
            }
          }
          else {
            if(institution_roles.indexOf(role) > -1) {
              disable_fields = false;
            }
          }
        }
        if(disable_fields) {
          fek = disable_field('fek');
          fek_posted_at = disable_field('fek_posted_at');
          starts_at = disable_field('starts_at');
          ends_at = disable_field('ends_at');
        }
        else {
          fek = 'fek';
          fek_posted_at = 'fek_posted_at';
          starts_at = 'starts_at';
          ends_at = 'ends_at';
        }
        return [fek, fek_posted_at, starts_at, ends_at];
      }),
      layout: {
        flex: [50, 50, 50, 50]
      }
    },
    candidacies: {
      label: 'candidacy.menu_label',
      fields: [candidaciesField(undefined, false, false)]
    },
    committee: {
      label: 'fieldsets.labels.committee',
      text: 'fieldsets.text.committee',
      fields: [
        fileField('committee_set_file', 'position', 'committee_set_file', {
          hint: 'committee_set_file.hint',
          disabled: computed('model.changeset.electors_meeting_to_set_committee_date', function(){
            let date = get(this, 'model.changeset.electors_meeting_to_set_committee_date');
            return !(date);
          })
        }, {
          preventDelete: true,
          replace: true
        }),
        committeeElectorsField('committee_internal', 'internal', false, true),
        committeeElectorsField('committee_external', 'external', false, true),
        fileField('committee_proposal', 'position', 'committee_proposal', {
          disabled: computed('model.changeset.committee_note', function(){
            return getFile(this,'committee_note')
          })
        }),
        fileField('committee_note', 'position', 'committee_note', {
          disabled: computed('model.changeset.committee_proposal', function(){
            return getFile(this,'committee_proposal')
          })
        }),
      ],
      layout: {
        flex: [100, 100, 100, 100, 100]
      }
    },
    electors: {
      label: 'fieldsets.labels.electors',
      fields: [
        fileField('electors_set_file', 'position', 'electors_set_file', {
        }, {
          preventDelete: true,
          replace: true
        }),
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_regular: {
      text: computed('model.department_dep_number', function(){
        let num = get(this, 'model.department_dep_number');
        if (num > 40) {
          return 'fieldsets.text.electors_regular_big';
        } else {
          return 'fieldsets.text.electors_regular_small';
        }
      }),
      label: 'electors_regular_members.label',
      fields: [
        committeeElectorsField('electors_regular_internal', 'internal', false, true),
        committeeElectorsField('electors_regular_external', 'external', false, true)
      ],
      layout: {
        flex: [100, 100]
      }
    },
    electors_substitite: {
      text: computed('model.department_dep_number', function(){
        let num = get(this, 'model.department_dep_number');
        if (num > 40) {
          return 'fieldsets.text.electors_sub_big';
        } else {
          return 'fieldsets.text.electors_sub_small';
        }
      }),
      label: 'electors_sub_members.label',
      fields: [
        committeeElectorsField('electors_sub_internal', 'internal', false, true),
        committeeElectorsField('electors_sub_external', 'external', false, true),
        field('electors_meeting_to_set_committee_date', {
          //hint: 'electors_meeting_to_set_committee_date.hint',
          disabled: computed(
                 'model.changeset.electors_regular_external',
                 'model.changeset.electors_regular_internal',
                 'model.changeset.electors_sub_external',
                 'model.changeset.electors_sub_internal',
                 'model.electors_regular_external.[]',
                 'model.electors_regular_internal.[]',
                 'model.electors_sub_external.[]',
                 'model.electors_sub_internal.[]',
                 'model.department_dep_number',
                      function() {

            let isInt = function(data) {
              return data === parseInt(data, 10);
            }

            let num = get(this, 'model.department_dep_number');

            let c_r_e = get(this, 'model.changeset.electors_regular_external').length;
            let c_r_i = get(this, 'model.changeset.electors_regular_internal').length;
            let c_s_e = get(this, 'model.changeset.electors_sub_external').length;
            let c_s_i = get(this, 'model.changeset.electors_sub_internal').length;

            let m_r_e = get(this, 'model').hasMany('electors_regular_external').ids().length;
            let m_r_i = get(this, 'model').hasMany('electors_regular_internal').ids().length;
            let m_s_e = get(this, 'model').hasMany('electors_sub_external').ids().length;
            let m_s_i = get(this, 'model').hasMany('electors_sub_internal').ids().length;

            let r_e =  isInt(c_r_e)? c_r_e: m_r_e;
            let r_i =  isInt(c_r_i)? c_r_i: m_r_i;
            let s_e =  isInt(c_s_e)? c_s_e: m_s_e;
            let s_i =  isInt(c_s_i)? c_s_i: m_s_i;

            let regular = (parseInt(r_e) || 0)+ (parseInt(r_i) || 0);
            let sub =  (parseInt(s_e) || 0) + (parseInt(s_i) || 0);

            if (num>40) {
              if (sub == 15 && regular == 15) {
                return false
              }
            } else {
              if (sub == 11 && regular == 11) {
                return false
              }
            }
            return true;
          })
        })

      ],
      layout: {
        flex: [100, 100, 100]
      }
    },
    election: {
      label: 'fieldsets.labels.election',
      fields: [
        fileField('electors_meeting_proposal', 'position', 'electors_meeting_proposal', {
        }, {
          preventDelete: true,
          replace: true,
        }),
        'electors_meeting_date',
        fileField('nomination_proceedings', 'position', 'nomination_proceedings', {
          hint: 'nomination_proceedings.hint',
          disabled: computed('model.changeset.electors_meeting_proposal',
                      'model.changeset.electors_meeting_date', function(){
            let date = get(this, 'model.changeset.electors_meeting_date');
            return !(date && getFile(this,'electors_meeting_proposal'));
          })
        }, {
          preventDelete: true,
          replace: true
        }),
        fileField('proceedings_cover_letter', 'position', 'proceedings_cover_letter', {
          hint: 'cover_letter.should.be.filled',
          disabled: computed('model.changeset.nomination_proceedings', function(){
            return !getFile(this,'nomination_proceedings');
          })
        }, {
          preventDelete: true,
          replace: true
        }),
        field('elected', {
          autocomplete: true,
          hint: 'cover_letter.should.be.filled',
          disabled: computed('model.changeset.nomination_proceedings', function(){
            return !getFile(this,'nomination_proceedings');
          }),
          query: function(table, store, field, params) {
            let position_id = get(field, 'model').get('id');
            let candidacies = store.query('candidacy', {position: position_id});
            let promise = candidacies.then((items) => {
              return Ember.RSVP.all(items.getEach('candidate'));
            });
            return DS.PromiseArray.create({promise});
          },
        }),
        field('second_best', {
          autocomplete: true,
          hint: 'cover_letter.should.be.filled',
          disabled: computed('model.changeset.nomination_proceedings', function(){
            return !getFile(this,'nomination_proceedings');
          }),
          query: function(table, store, field, params) {
            let position_id = get(field, 'model').get('id');
            let candidacies = store.query('candidacy', {position: position_id});
            let promise = candidacies.then((items) => {
              return Ember.RSVP.all(items.getEach('candidate'));
            });
            return DS.PromiseArray.create({promise});
          },
        }),
        fileField('nomination_act', 'position', 'nomination_act', {
          hint: 'nomination_act.hint',
          disabled: computed('model.changeset.proceedings_cover_letter',
            'model.changeset.revocation_decision',
            'model.changeset.failed_election_decision', function(){
            let cover = getFile(this,'proceedings_cover_letter');
            let revocation = getFile(this,'revocation_decision');
            let failed = getFile(this,'failed_election_decision');
            return !cover || revocation || failed;
          })
        }),
        field('nomination_act_fek', {
          hint: 'nomination_act.hint',
          disabled: computed('model.changeset.proceedings_cover_letter',
            'model.changeset.revocation_decision',
            'model.changeset.failed_election_decision', function(){
            let cover = getFile(this,'proceedings_cover_letter');
            let revocation = getFile(this,'revocation_decision');
            let failed = getFile(this,'failed_election_decision');
            return !cover || revocation || failed;
          })
        }),
        fileField('revocation_decision', 'position', 'revocation_decision', {
          hint: 'cannot.be.filled.if.nomination',
          disabled: computed('model.changeset.nomination_act_fek',
                      'model.changeset.failed_election_decision',
                      'model.changeset.nomination_act', function(){
            let nomination = getFile(this,'nomination_act');
            let fek = get(this, 'model.changeset.nomination_act_fek');
            let failed = getFile(this,'failed_election_decision');
            return fek || nomination || failed;
          })
        }),
        fileField('failed_election_decision', 'position', 'failed_election_decision', {
          hint: 'cannot.be.filled.if.nomination',
          disabled: computed('model.changeset.nomination_act_fek',
                      'model.changeset.revocation_decision',
                      'model.changeset.nomination_act', function(){
            let nomination = getFile(this,'nomination_act');
            let fek = get(this, 'model.changeset.nomination_act_fek');
            let revocation = getFile(this,'revocation_decision');
            return fek || nomination || revocation;
          })
        }),
      ],
      layout: {
        flex: [100, 100, 100, 100, 50, 50, 100, 100, 100, 100]
      }
    },

    assistant_files: {
      label: 'fieldsets.labels.assistant_files',
      fields: [
        fileField('assistant_files', 'position', 'assistant_files', {
        }, {
          multiple: true
        }),
      ]
    },

  }
};

export {position};
