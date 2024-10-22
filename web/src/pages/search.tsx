import SearchNote from '../models/search_note';
import { useLoaderData } from 'react-router-dom';
import { useData } from '../utils/fetcher';
import Note from '../models/note';
import SearchResults from '../components/search_result';

export async function loader({ params }: any) {
  let searchNote = SearchNote.fromUrlQuery(params.searchParams)

  return { searchNote }
}

export default function SearchComponent() {
  const { searchNote } = useLoaderData() as {searchNote: SearchNote};
  const { data, error, loading } = useData<Note[]>(...searchNote.toGetNotesRequest());

  if (loading) {
    return <div>Loading</div>
  } else if (error) {
    return <div>{error.message}</div>
  }

  return <div>
    <SearchResults notes={data} />    
  </div>
}