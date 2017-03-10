import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator, preloadRelations} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';
import {
  goToDetails, applyCandidacy, positionActions
} from 'ui/utils/common/actions';
import {pick_edit_fs, pick_details_fs, pick_create_fs} from 'ui/lib/position/pick_fs_functions';
import {abilityStates} from 'ui/lib/position/abilityStates';

/*
 * This gen is used for displaying:
 * - Helpdesk admins, helpdesk users: all positions, in all states
 * - Institution managers: positions of their institution, in all states
 * - Assistants: positions of their departments, in all states
 * - Professors: positions of their department, in all states
 */

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

export default ApellaGen.extend({
  order: 800,
  modelName: 'position',
  resourceName: 'positions',
  auth: true,
  path: 'positions',

  abilityStates: abilityStates,

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:3, max:200})],
      description: [validate.presence(true), validate.length({max:4000})],

      /*
       * Heldesk admin can modify starts_at, ends_at dates without any client
       * side constrains.
       */

      starts_at: computed('role', function() {
        let role = get(this, 'role');

        if(role === 'helpdeskadmin') {
          return [];
        }
        else  {
          return [afterToday()];
        }
      }),
      ends_at:  computed('role', function() {
        let role = get(this, 'role');
        if(role === 'helpdeskadmin') {
          return [];
        }
        else  {
          return [afterDays({on:'starts_at', days:30})];
        }
      }),
      fek_posted_at: [beforeToday()],
      fek: urlValidator,
      discipline: [validate.presence(true)],
      subject: [validate.presence(true)],
      subject_area: [validate.presence(true)],
      // electors_meeting_to_set_committee_date: [afterToday()],
      department_dep_number: [validate.presence(true), validate.number({integer: true})]
    }
  },
  create: {
    onSubmit(model) {
      this.transitionTo('position.record.index', model);
    },
    fieldsets: pick_create_fs(),
  },
  list: {
    getModel: function(params) {
      params = params || {};
      let user = get(this, 'session.session.authenticated'),
        role = user.role;
      if(role === 'professor') {
        if (user.department) {
          let department_id = user.department.split('/').slice(-2)[0];
          params.department = department_id;
        }
      }
      return this.store.query('position', params);
    },
    sort: {
      active: true,
      fields: ['code', 'title', 'old_code'],
      serverSide: true
    },
    filter: {
      active: true,
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder_positions',
      meta: {
        fields: computed('user.role', function() {
          let user_role = get(this, 'user.role'),
            roles_institution = ['helpdeskadmin', 'helpdeskuser'],
            roles_department = ['institutionmanager', 'assistant'],
            filter_model, dataKey, user_institution;

          if (user_role === 'professor') {
            return ['state_expanded'];
          }
          else if (roles_institution.indexOf(user_role) > -1) {
            filter_model = 'institution';
            dataKey = 'department__institution';
          }
          else if (roles_department.indexOf(user_role) > -1) {
            filter_model = 'department';
            dataKey = 'department';
            user_institution = get(this, 'user.institution').split('/').slice(-2)[0];
          }
          return [
            field(filter_model, {
              autocomplete: true,
              type: 'model',
              modelName: filter_model,
              displayAttr: 'title_current',
              dataKey: dataKey,
              query: function(select, store, field, params) {
                let locale = get(select, 'i18n.locale'),
                  ordering_param = `title__${locale}`;
                params = params || {};
                params.ordering = ordering_param;
                if(filter_model === 'institution'){
                  params.category = 'Institution';
                }
                else if (filter_model === 'department') {
                  params.institution = user_institution;
                }
                return store.query(filter_model, params)
              }
            }),
            'state_expanded'
          ]
        })
      }
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'event_available',
      label: computed(function() {
        let role = get(this, 'session.session.authenticated.role');
        if (role === 'professor'){
          return 'position_department.menu_label';
        }
        else {
          return 'position.menu_label';
        }
    }),
      display: computed('role', function() {
        let role = get(this, 'role'),
          is_foreign = get(this, 'session.session.authenticated.is_foreign'),
          rank = get(this, 'session.session.authenticated.rank') || '',
          is_researcher = rank.match(/research/i);

        if (role === 'candidate' || (role === 'professor' && is_foreign) || (role === 'professor' && is_researcher)) {
          return false;
        }
        else {
          return true;
        }
      })
    },
    layout: 'table',
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let f = [
          field('code', { dataKey: 'id' }), 'old_code', 'title', 'state_calc_verbose',
          field('department.title_current', {label: 'department.label'}),
        ];
        if (!(role == 'institutionmanager' || role == 'assistant')) {
          f.pushObject(field('institution.title_current'));
        }
        return f;
      }),

      actions: ['gen:details','applyCandidacy', 'gen:edit', 'remove', 'cancelPosition', 'setElecting', 'setRevoked', 'setFailed', 'setSuccessful' ],
      actionsMap: {
        applyCandidacy: applyCandidacy,
        cancelPosition: positionActions.cancelPosition,
        setElecting: positionActions.setElecting,
        setRevoked: positionActions.setRevoked,
        setFailed: positionActions.setFailed,
        setSuccessful: positionActions.setSuccessful,
      }
    }
  },
  edit: {
    fieldsets: computed('role', 'model.state', 'model.starts_at', 'model.ends_at', pick_edit_fs),
  },
  details: {
    /*
     * for details view should preload candidacies in order to run checks and
     * decide if the candidacies fs should be rendered.
     */
    getModel(params, model) {
      let position_id = get(model, 'id'),
        store = get(model, 'store'),
        query = {
          position: position_id,
          latest: true
        };

      return store.query('candidacy', query).then(function() {
        return model;
      });
    },
    actions: computed('model.is_latest', function() {
      let is_latest = get(this, 'model.is_latest');
      if (is_latest) { return ['gen:edit']; }
      return [];
    }),
    page: {
      title: computed('model.code', 'model.is_latest', function() {
        let code = get(this, 'model.code');
        let latest = get(this, 'model.is_latest');
        if (!latest) {
          let label = get(this, 'model.i18n').t('position.history.label');
          code = code += ` (${label})`;
        }
        return code;
      })
    },
    partials: {
      top: 'position-top'
    },
    fieldsets: computed('role', 'user.id', 'user.user_id', 'model.state', 'model.starts_at', 'model.ends_at', pick_details_fs),
  }
});
