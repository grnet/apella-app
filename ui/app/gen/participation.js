import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';

const {
  computed,
  get,
  assign
} = Ember;


export default ApellaGen.extend({
  order: 200,
  name: 'participations',
  resourceName: 'positions',
  path: 'participations',


  page: {
    title: 'elections.menu_label',
  },
  list: {
    page: {
      title: 'elections.menu_label',
    },
    getModel(params, model) {
      params = params || {};
      // Server side pagination and ordering cannot be applied in this view
      delete params.limit;
      delete params.offset;
      delete params.ordering;

      let id = get(this, 'session.session.authenticated.id');
      let query_electors = {};
      let query_committee = {};

      assign(query_electors, {electors: id}, params);
      assign(query_committee, {committee: id}, params);

      let promises = [
        get(this, 'store').query('position', query_electors),
        get(this, 'store').query('position', query_committee),
      ]
      var promise = Ember.RSVP.all(promises).then(function(arrays) {
        var mergedArray = Ember.A();
        arrays[0].forEach(function(el) {
          el.set('participation', 'Elector');
        })
        arrays[1].forEach(function(el) {
          el.set('participation', 'Committee');
        })
        arrays.forEach(function (records) {
          mergedArray.pushObjects(records.toArray());
        });
        return mergedArray.uniqBy('id')
      });

      return DS.PromiseArray.create({
        promise: promise,
      });
    },
    filter: {
      active: true,
      serverSide: true,
      search: true,
      searchPlaceholder: 'search.placeholder_positions',
      meta: {
        fields: [
          field('institution', {
            autocomplete: true,
            type: 'model',
            modelName: 'institution',
            displayAttr: 'title_current',
            dataKey: 'department__institution',
            query: function(select, store, field, params) {
              let locale = get(select, 'i18n.locale'),
                ordering_param = `title__${locale}`;
              params = params || {};
              params.ordering = ordering_param;
              params.category = 'Institution';

              return store.query('institution', params)
            }
          }),
        ]
      }
    },
    menu: {
      icon: 'assignment',
      label: 'elections.menu_label',
      display: computed('role', function(){
        let role = get(this, 'role');
        let rank = get(this, 'session.session.authenticated.rank');
        let forbiddenRanks = ['Lecturer', 'Tenured Assistant Professor'];
        let allowedRanks = !forbiddenRanks.includes(rank);
        return (role == 'professor' && allowedRanks);
      }),
    },
    layout: 'table',
    row: {
      fields: ['code', 'old_code', 'title', 'state_calc_verbose',
              'discipline', 'participation_current',
              field('department.institution.title_current', {label: 'institution.label'}),
              field('department.title_current', {label: 'department.label'})],
      actions: ['goToDetails'],
      actionsMap: {
        goToDetails: {
          label: 'viewPosition',
          icon: 'visibility',
          action(route, model){
            route.transitionTo('position.record.index', model);
          }
        }
      },
    }
  }
});
