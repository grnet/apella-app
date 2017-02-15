import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    electors_meeting_proposal: embedded,
    nomination_proceedings: embedded,
    proceedings_cover_letter: embedded,
    nomination_act: embedded,
    revocation_decision: embedded,
    failed_election_decision: embedded,
    electors_meeting_proposal: embedded,
    assistant_files: embedded,
    electors_set_file: embedded
  }
});
