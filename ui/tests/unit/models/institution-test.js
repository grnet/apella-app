import { moduleForModel, test } from 'ember-qunit';

moduleForModel('institution', 'Unit | Model | institution', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject({
    id: 1,
    title: 'institution title',
  });
  // let store = this.store();
  assert.ok(!!model);
});
