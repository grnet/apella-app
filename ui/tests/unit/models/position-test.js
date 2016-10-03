import { moduleForModel, test } from 'ember-qunit';

moduleForModel('position', 'Unit | Model | position', {
  // Specify the other units that are required for this test.
  needs: ["model:subject", "model:subject-area", "model:user", "model:department"]
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});
