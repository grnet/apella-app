import {field} from 'ember-gen';
import {ApellaGen} from 'ui/lib/common';
import gen from 'ember-gen/lib/gen';

const {
  computed,
  get,
} = Ember;


export default ApellaGen.extend({
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
    getModel() {
      let id = get(this, 'session.session.authenticated.id');
      let promises = [
        get(this, 'store').query('position', {electors: id}),
        get(this, 'store').query('position', {committee: id}),
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
    menu: {
      icon: 'drafts',
      label: 'elections.menu_label',
      display: computed('role', function(){
        let role = get(this, 'role')
        return (role=== 'professor');
      }),
    },
    layout: 'table',
    row: {
      fields: ['code', 'title', 'state_verbose',
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
