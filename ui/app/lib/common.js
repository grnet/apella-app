import Ember from 'ember';
import {CRUDGen} from 'ember-gen/lib/gen';
import ENV from 'ui/config/environment';

const {
  computed: { reads }
} = Ember;

const ApellaGen = CRUDGen.extend({
  auth: true,
  resourceName: reads('path'),
  list: {
    paginate: {
      limits: [10, 40, 100],
      serverSide: true,
      active: true
    }
  }
});

export {
  ApellaGen
}
