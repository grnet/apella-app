import Ember from 'ember';
import DS from 'ember-data';

const {
  RSVP: { Promise },
  assert,
  get,
  set,
  isArray,
  observer,
  computed,
  computed: { alias, equal, gt, map }
} = Ember;



export default Ember.Component.extend({
  tagName: 'div',
  classNames: ['md-no-style', 'md-list-item-inner'],
  classNameBindings: ['partiallySelected:partial'],

  store: Ember.inject.service(),
  expanded: false,
  partiallySelected: false,

  rootIsSelected: computed('item', 'selected.[]', function(){
    return get(this, 'selected').includes(get(this, 'item'));
  }),

  toggleIcon: computed('expanded', function(){
    return this.get('expanded')? 'expand-more': 'chevron-right'
  }),

  observeRoot: observer('rootIsSelected', 'expanded', function(){
    let expanded = get(this, 'expanded');
    let subModelType = get(this, 'subModelType');
    let rootIsSelected = get(this, 'rootIsSelected');
    if (expanded && rootIsSelected ) {
      let nodes = get(this, 'nodes');
      nodes.then( () => {
        nodes.forEach( (el) => {
          this.sendAction('onChange', false, el, subModelType);
        })
      })
    }
  }),

  observeNodes: observer('subSelected.[]', 'expanded', 'item',  function(){
    let subSelected = get(this, 'subSelected');
    let expanded = get(this, 'expanded');
    let type = get(this, 'modelType');
    if (type=='subject-area') { type = 'area' }
    let el = get(this, 'item');
    let self = this;

    if (expanded) {
      let nodes = get(this, 'nodes');
      nodes.then( () => {
        let nodesNum = get(nodes, 'length');
        if (nodesNum>0) {
          let cnt = 0;
          nodes.forEach( (el) => {
            if ( subSelected.includes(el) ) {
              cnt = cnt + 1;
            }
          })
          if (cnt == 0) {
            set(self, 'partiallySelected', false);
            this.sendAction('onChange', true, el, type);
          } else if (cnt == nodesNum) {
            set(self, 'partiallySelected', false);
            self.sendAction('onChange', false, el, type);
          } else {
            set(self, 'partiallySelected', true);
            this.sendAction('onChange', true, el, type);
          }
        }
      });
    }

  }),

  nodes: computed('', function(){
    let subModelType = get(this, 'subModelType');
    let query = {};
    query['ordering'] = 'id';
    query[get(this, 'lookupField')] = get(get(this, 'item'), 'id');
    return this.get('store').query(subModelType, query);

  }),

  actions: {
    toggle(item) {
      this.toggleProperty('expanded');
    },
    handleChange(value, item, modelType, subModelType) {
      let type = modelType;
      let self = this;
      if (modelType=='subject-area') { type = 'area' }
      if (subModelType) {
        let nodes = get(this, 'nodes');
        nodes.forEach(function(el){
          self.sendAction('onChange', value, el, subModelType);
        });
      }
      this.sendAction('onChange', value, item, type);
    }
  }

});
