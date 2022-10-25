import './App.css';
import { Route, Routes, BrowserRouter } from "react-router-dom"
import { HomePage } from './pages/HomePage';
import { MenuPage } from './pages/MenuPage';
import { MenuModePage } from './pages/MenuModePage';
import { ModePage } from './pages/ModePage';
import { Navbar } from './components/Navbar';
import { FinishGamePage } from './pages/FinishGamePage';

function App() {
  return (
    <>
    <BrowserRouter>
      <Navbar></Navbar>
      
      <Routes>
        <Route path='/' element={<HomePage></HomePage>}></Route>
        <Route path='/menu' element={<MenuPage></MenuPage>}></Route>
        <Route path='/menu/:mode' element={<MenuModePage></MenuModePage>}></Route>
        <Route path='/menu/:mode/play' element={<ModePage></ModePage>}></Route>
        <Route path='/menu/:mode/finishgame' element={<FinishGamePage></FinishGamePage>}></Route>
      </Routes>
    </BrowserRouter>
    </>
  );
}

export default App;
