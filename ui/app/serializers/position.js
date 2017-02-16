import DS from 'ember-data';
import Serializer from './application';

const embedded = { embedded: 'always' };

export default Serializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    assistant_files: embedded,
    committee_note: embedded,
    committee_proposal: embedded,
    committee_set_file: embedded,
    electors_meeting_proposal: embedded,
    electors_meeting_proposal: embedded,
    electors_set_file: embedded,
    failed_election_decision: embedded,
    nomination_act: embedded,
    nomination_proceedings: embedded,
    proceedings_cover_letter: embedded,
    revocation_decision: embedded,
  }
});
