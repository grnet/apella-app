import {field} from 'ember-gen';
import {disable_field} from 'ui/utils/common/fields';
import {ApellaGen, urlValidator} from 'ui/lib/common';
import validate from 'ember-gen/validate';
import gen from 'ember-gen/lib/gen';
import {afterToday, beforeToday, afterDays} from 'ui/validators/dates';
import moment from 'moment';
import {
  goToDetails, applyCandidacy
} from 'ui/utils/common/actions';
import {pick_details_fs} from 'ui/lib/position/pick_fs_functions';
import {abilityStates} from 'ui/lib/position/abilityStates';

/*
 * This gen is used for displaying:
 * - Candidates: positions in state posted
 * - Professors: positions in state posted
 */

const {
  computed,
  computed: { reads },
  get,
  merge, assign
} = Ember;

export default ApellaGen.extend({
  order: 170,
  name: 'positions-latest',
  modelName: 'position',
  resourceName: 'positions',
  auth: true,
  path: 'positions-latest',

  abilityStates: abilityStates,

  common: {
    validators: {
      title: [validate.presence(true), validate.length({min:3, max:200})],
      description: [validate.presence(true), validate.length({max:300})],

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
      department_dep_number: [validate.presence(true), validate.number({integer: true})]
    }
  },
  create: {
    routeMixins: {
      beforeModel(transition) {
        return this.transitionTo('position.create.index')
      }
    }
  },
  list: {
    getModel: function(params) {
      params = params || {};
      params.state_expanded = 'before_closed';
      if(!params.ordering) {
        params.ordering = '-id';
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
      meta: {
        fields: [
          field('institution', {
            autocomplete: true,
            type: 'model',
            displayAttr: 'title_current',
            modelName: 'institution',
            dataKey: 'department__institution',
            query: function(select, store, field, params) {
              let locale = get(select, 'i18n.locale'),
                ordering_param = `title__${locale}`;
              params = params || {};
              params.category = 'Institution';
              params.ordering = ordering_param;
              return store.query('institution', params)
            }
          }),
        ]
      },
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder_positions'
    },
    page: {
      title: 'position.menu_label',
    },
    menu: {
      icon: 'search',
      label: 'position_search.menu_label',
      display: computed('role', function() {
        let role = get(this, 'role');
        if (['professor', 'candidate'].indexOf(role) > -1) {
          return true;
        }
        else {
          return false;
        }
      })
    },
    row: {
      fields: computed('role', function(){
        let role = get(this, 'role');
        let f = [
          field('code', { dataKey: 'id' }), 'old_code', 'title', 'rank_verbose', 'state_calc_verbose',
          field('department.title_current', {label: 'department.label'}),
        ];
        if (!(role == 'institutionmanager' || role == 'assistant')) {
          f.pushObject(field('institution.title_current'));
        }
        return f;
      }),

      actions: ['gen:details','applyCandidacy', 'remove'],
      actionsMap: {
        applyCandidacy: applyCandidacy,
      }
    }
  },
  edit: {
    routeMixins: {
      afterModel(model, transition) {
        this.transitionTo('position.record.edit.index', model.get('id'))
      }
    }
  },
  details: {
    /*
     * for details view should preload candidacies in order to run checks and
     * decide if the candidacies fs should be rendered.
     */
    getModel(params, model) {
      let position_id = get(model, 'id'),
        store = get(model, 'store'),
        query = { position: position_id };

      return store.query('candidacy', query).then(function() {
        return model;
      });
    },
    page: {
      title: computed.readOnly('model.code')
    },
    fieldsets: computed('role', 'user.id', 'user.user_id', 'model.state', 'model.starts_at', 'model.ends_at', 'model.position_type',  pick_details_fs),
  }
});
