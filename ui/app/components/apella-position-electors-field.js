import Ember from 'ember';
import TableSelectField from 'ember-gen/components/gen-form-field-select-table/component';
const { observer, get } = Ember;

function asProfessor(item) {
  let professor = item;
  if (item.constructor.modelName.indexOf('registry-member') == 0) {
    professor = item.asProfessor();
  }
  return professor;
}


export default TableSelectField.extend({

  // Patch a custom `includes` method for value array.
  // The custom method matches `user_id` against list `ids` 
  // when registry-member instance is passed as argument.
  setupValue: observer('value', function() {
    let value = get(this, 'value');
    if (value) {
      let addObject = value.addObject;
      value.addObject = function(item) {
        return addObject.apply(value, [asProfessor(item)]);
      }
      let removeObject = value.removeObject;
      value.removeObject = function(item) {
        return removeObject.apply(value, [asProfessor(item)]);
      }
      value.includes = function(item) {
        if (item && item.constructor.modelName.indexOf('registry-member') == 0) {
          let ids = value.getEach('id').map(String);
          return ids.includes(item.get('professor_id') + '');
        }
      }
    }
  })
});
