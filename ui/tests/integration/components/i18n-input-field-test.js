import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('i18n-input-field', 'Integration | Component | i18n input field', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{i18n-input-field}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#i18n-input-field}}
      template block text
    {{/i18n-input-field}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
