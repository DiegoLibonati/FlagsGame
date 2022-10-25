import React from 'react'
import { useContext } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { FlagsContext } from '../context/FlagsContext'
import { Hamburger } from './Hamburger'
import "./Navbar.css"

export const Navbar = () => {

    const {navbar, manageNavbar} = useContext(FlagsContext)

  return (
    <header className='header_container'>
        <div className='header_container_logo'>
            <Link to="/">
                FlagsGame
            </Link>

            <Hamburger navbar={navbar} manageNavbar={manageNavbar}></Hamburger>
        </div>

        <nav className={navbar ? 'header_container_nav open-nav' : 'header_container_nav'}>
            <ul className='header_container_nav_list'>
                <li>                
                    <NavLink to="/" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Home</NavLink>
                </li>
                <li>
                    <NavLink to="/menu" className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>Menu</NavLink>
                </li>
            </ul>
        </nav>
    </header>
  )
}
