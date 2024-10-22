import React from 'react';
import { Box, Button, Textarea } from '@chakra-ui/react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateNote from '../models/create_note';
import Note from '../models/note';
import { fetchRpc } from '../utils/fetcher';

const CreateComponent: React.FC = () => {
    const navigate = useNavigate();
    const [text, setText] = useState("");

    const submitNote = async () => {
      const createNote = new CreateNote(text);
      const note = await fetchRpc<Note>(...createNote.toCreateRequest());

      navigate("/note/" + note.id);
    }

    return (
      <Box
        style={{
          display: "flex",
          flexDirection: "column",
          height: "calc(100vh - 50px)", // adjust 50px based on height of other elements
        }}
      >
        <Textarea
          style={{ flexGrow: 1, minHeight: 0 }}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder='Note text'
        />
        <Box style={{ display: "flex", flexDirection: "row", width: "100%" }}>
          <Button width="10%" style={{ flexShrink: 0 }} colorScheme="red">Record</Button>
          <Button width="90%" style={{ flexShrink: 0 }} colorScheme="gray" onClick={submitNote}>Submit</Button>
        </Box>
      </Box>
    );
}

export default CreateComponent;
