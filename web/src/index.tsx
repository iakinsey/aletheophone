import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  Router,
  RouterProvider,
} from "react-router-dom";
import SearchComponent, {loader as searchLoader} from './pages/search';
import NoteComponent, {loader as noteLoader} from './pages/note';
import CreateComponent from './pages/create';
import { ChakraProvider } from '@chakra-ui/react';
import BaseLayout from './components/base';

const router = createBrowserRouter([
  {
    path: "/",
    element: <BaseLayout />,
    children: [
      {
        path: "",
        element: <SearchComponent />,
        loader: searchLoader
      },
      {
        path: "search",
        element: <SearchComponent />,
        loader: searchLoader
      },
      {
        path: "search/:searchParams",
        element: <SearchComponent />,
        loader: searchLoader
      },
      {
        path: "note/:noteId",
        element: <NoteComponent />,
        loader: noteLoader
      },
      {
        path: "create",
        element: <CreateComponent />
      }
    ]
  }
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>
);