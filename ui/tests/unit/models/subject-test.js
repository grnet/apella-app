import { moduleForModel, test } from 'ember-qunit';

moduleForModel('subject', 'Unit | Model | subject', {
  // Specify the other units that are required for this test.
  needs: ["model:subject-area"]
});

test('it exists', function(assert) {
  let model = this.subject({
    id: 1,
    title: 'subject title',
  });
  // let store = this.store();
  assert.ok(!!model);
});
