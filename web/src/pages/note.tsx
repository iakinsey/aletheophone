import { useLoaderData } from 'react-router-dom';
import GetNote from '../models/get_note';
import { useData } from '../utils/fetcher';
import Note from '../models/note';

export async function loader({ params }: any) {
  let getNote = new GetNote(Number(params.noteId));

  return { getNote }
}


export default function NoteComponent() {
  const { getNote } = useLoaderData() as {getNote: GetNote};
  const { data, error, loading } = useData<Note>(...getNote.toGetRequest());

  if (loading) {
    return <div>Loading</div>
  } else if (error) {
    return <div>{error.message}</div>
  }

  return <div>{data?.text ? data.text : "No note text"}</div>
}