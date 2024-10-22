import { Table, TableContainer, Tbody, Td, Tr } from "@chakra-ui/react";
import Note from "../models/note";
import { Link } from "react-router-dom";

interface SearchResultProps {
    notes: Note[] | undefined
}



const SearchResults: React.FC<SearchResultProps> = ({ notes }) => {
    return (
        <TableContainer>
            <Table>
                <Tbody>
                    {notes?.map((note) => (
                        <Tr key={note.id}>
                            <Td>
                                <Link to={"/note/" + note.id}>
                                    {note.text.length <= 128 ? note.text : note.text.slice(0, 128) + "..."}
                                </Link>
                            </Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>
    );
}

export default SearchResults;