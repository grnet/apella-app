import { faker, Factory } from 'ember-cli-mirage';

export default Factory.extend({
  username() { return faker.internet.userName(); },
  last_name() { return faker.name.lastName(); },
  first_name() { return faker.name.firstName(); },
  state: 'Active'
});
