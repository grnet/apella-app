import { moduleForModel, test } from 'ember-qunit';

moduleForModel('department', 'Unit | Model | department', {
  // Specify the other units that are required for this test.
  needs: ["model:school"]
});

test('it exists', function(assert) {
  let model = this.subject({
    id: 1,
    title: 'department title',
  });
  // let store = this.store();
  assert.ok(!!model);
});
