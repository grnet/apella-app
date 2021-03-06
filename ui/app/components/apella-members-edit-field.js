import Ember from 'ember';
import TableSelectField from 'ember-gen/components/gen-form-field-select-table/component';

const {
  computed,
  get, set,
  on,
  observer
} = Ember;

export default TableSelectField.extend({
  activeSubTable: 'add',
  removeMembers: computed('value.remove', function() { return get(this, 'value.remove') || Ember.A([]); }),
  addMembers: computed('value.add', function() { return get(this, 'value.add') || Ember.A([]); }),
  inRegistryMembers: computed('value', function() {
    let registry_id = parseInt(get(this, 'form.model.id'));
    let members = Ember.A();
    // hacky trick
    members.includes = function(professor) {
      // do check if registry is included in registries
      let professor_registries = get(professor, 'registries').replace('\"', '') ;
      try {
           professor_registries = JSON.parse(professor_registries).map(String)
      } catch(err) {
        professor_registries = [];
      }
      return professor_registries.includes(registry_id+ '')
    }
    return members;
  }),
  allMembers: computed('value', function(){
    return [];
  }),
  removeRowGen: computed('gen.rowGen', function() {
    let component = this;
    return get(this, 'gen.rowGen').extend({
      actions: ['cancel'],
      actionsMap: {
        cancel: {
          label: 'restore',
          icon: 'undo',
          action: function() { component.send('cancelRemove', ...arguments); },
          permissions: [],
          warn: true,
          confirm: true,
          prompt: {
            title: 'row.restore.confirm.title',
            message: 'row.restore.confirm.message',
            ok: 'row.restore.confirm.ok',
            cancel: 'cancel'
          }
        }
      }
    });
  }),

  actions: {

    cancelRemove(item, model) {
      let value = get(this, 'value');
      let value_remove = get(this, 'value.remove') || [];

      value_remove.removeObject(model);
      this.onChange(value);
    },

    handleItemRemove(item, model) {
      /*
       * @param {route} item: registry record edit route (unused)
       * @param {model} model: registry-member model to be removed
       * */

      let removeMembers = get(this, 'removeMembers');
      let addMembers = get(this, 'addMembers');
      let value_remove = get(this, 'value.remove') || [];
      let value_add = get(this, 'value.add') || [];
      let value = get(this, 'value');

      if (addMembers.includes(model)) {
        value_add.removeObject(model);
        return false;
      }

      if (!removeMembers.includes(model)) {
        value_remove.addObject(model);
        this.onChange(value);
      }

      return false;
    },

    handleAddItems(items) {

      let value_add = get(this, 'value.add') || [];
      let value = get(this, 'value');
      let addMembers = get(this, 'addMembers');
      let removeMembers = get(this, 'removeMembers');

      items.forEach((item) => {
        if (!addMembers.includes(item)) {
          value_add.addObject(item);
        }
      });

      this.onChange(value);
      set(this, 'showOptions', false);
    },

    hideOptions: function() {
      set(this, 'showOptions', false);
      set(this, 'allMembers', get(this, 'value.add'));
    }
  }
});
