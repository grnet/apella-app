import { Model } from 'ember-cli-mirage';

export default Model.extend({
  username: DS.attr(),
  last_name: DS.attr(),
  first_name: DS.attr(),
  status: DS.attr()
});
