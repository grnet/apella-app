import { moduleForModel, test } from 'ember-qunit';

moduleForModel('school', 'Unit | Model | school', {
  // Specify the other units that are required for this test.
  needs: ["model:institution"]
});

test('it exists', function(assert) {
  let model = this.subject({
    id: 1,
    title: 'school title',
  });
  // let store = this.store();
  assert.ok(!!model);
});
