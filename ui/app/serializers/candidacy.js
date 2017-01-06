import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always', serialize: 'ids' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    diplomas: embedded,
    publications: embedded,
    cv: embedded,
  }
});
