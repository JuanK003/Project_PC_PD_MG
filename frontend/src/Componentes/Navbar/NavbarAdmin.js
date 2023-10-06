import { Fragment } from 'react'
import { Popover, Transition } from '@headlessui/react'
import {
  ArrowPathIcon,
  Bars3Icon,
  BookmarkSquareIcon,
  CalendarIcon,
  ChartBarIcon,
  CursorArrowRaysIcon,
  LifebuoyIcon,
  PhoneIcon,
  PlayIcon,
  ShieldCheckIcon,
  Squares2X2Icon,
  XMarkIcon,
  ComputerDesktopIcon
} from '@heroicons/react/24/outline'
import { ChevronDownIcon } from '@heroicons/react/20/solid'
import axios from "axios";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";

const URI='https://store-online-mysql.herokuapp.com/Sucursales/'

const solutions = [
  {
    name: 'Registro de Usuarios',
    
    href: '/Usuarios',
    icon: Squares2X2Icon,
  },
  {
    name: 'Registros de Codigos-Postales',
 
    href: '/Codigos',
    icon: Squares2X2Icon,
  },
  { name: 'Registros de Municipalidades', 
 
  href: '/Municipios', 
  icon: Squares2X2Icon },
  {
    name: 'Registro de Departamentos',

    href: '/Departamentos',
    icon: Squares2X2Icon,
  },
]
const callsToAction = [
  { name: 'Ayuda...', href: '#', icon: Squares2X2Icon },
]
const resources = [
  {
    name: 'Chimaltenango',
    description: 'Centro comercial Pradera Chimaltenango.',
    href: '#',
    icon: Squares2X2Icon,
  },
  {
    name: 'Escuintla',
    description: 'Pradera Escuintla',
    href: '#',
    icon: Squares2X2Icon,
  },
  {
    name: 'Mazatenango',
    description: 'Las Américas en Mazatenango.',
    href: '#',
    icon: Squares2X2Icon,
  },
  { name: 'Coatepeque',
   description: 'La Trinidad en Coatepeque.',
    href: '#',
    icon: Squares2X2Icon },
    { name: 'Quetzaltenango',
   description: 'Pradera Xela en Quetzaltenango.',
    href: '#',
    icon: Squares2X2Icon },
    { name: 'Guatemala',
   description: 'Centro Comercial Miraflores en Ciudad de Guatemala.',
    href: '#',
    icon: Squares2X2Icon },

]
const recentPosts = [
 
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const CompNavBarAdmin =() => {

  
  

  return (
    <Popover className="relative bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex items-center justify-between border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
          <div className="flex justify-start lg:w-0 lg:flex-1">
            <a href="/">
              <span className="sr-only">Your Company</span>
              <img
                className="h-8 w-auto sm:h-10"
                src="https://c8.alamy.com/compes/2hf1k8m/vector-de-balon-de-futbol-de-futbol-rapido-y-llameante-aislado-sobre-fondo-blanco-2hf1k8m.jpg"
                alt=""
              />
            </a>
          </div>
          <div className="-my-2 -mr-2 md:hidden">
            <Popover.Button className="inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
              <span className="sr-only">Open menu</span>
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </Popover.Button>
          </div>
          <Popover.Group as="nav" className="hidden space-x-10 md:flex">
           

            <a href="/Equipos" className="text-base font-medium text-gray-500 hover:text-gray-900">
              EQUIPOS
            </a>
            <a href="/Torneos" className="text-base font-medium text-gray-500 hover:text-gray-900">
              TORNEOS
            </a>
            <a href="/Jugadores" className="text-base font-medium text-gray-500 hover:text-gray-900">
              JUGADORES
            </a>
            
          

            
          </Popover.Group>
          <div className="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
            <a href="/IniciarSesion" className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900">
              
            </a>
            <a
              href="/RegistrarseCliente"
               >
          
            </a>
          </div>
        </div>
      </div>

      <Transition
        as={Fragment}
        enter="duration-200 ease-out"
        enterFrom="opacity-0 scale-95"
        enterTo="opacity-100 scale-100"
        leave="duration-100 ease-in"
        leaveFrom="opacity-100 scale-100"
        leaveTo="opacity-0 scale-95"
      >
        <Popover.Panel focus className="absolute inset-x-0 top-0 origin-top-right transform p-2 transition md:hidden">
          <div className="divide-y-2 divide-gray-50 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5">
            <div className="px-5 pt-5 pb-6">
              <div className="flex items-center justify-between">
                <div>
                  <img
                    className="h-8 w-auto"
                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
                    alt="Your Company"
                  />
                </div>
                <div className="-mr-2">
                  <Popover.Button className="inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                    <span className="sr-only">Close menu</span>
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </Popover.Button>
                </div>
              </div>
              <div className="mt-6">
                <nav className="grid gap-y-8">
                  {solutions.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      className="-m-3 flex items-center rounded-md p-3 hover:bg-gray-50"
                    >
                      <item.icon className="h-6 w-6 flex-shrink-0 text-indigo-600" aria-hidden="true" />
                      <span className="ml-3 text-base font-medium text-gray-900">{item.name}</span>
                    </a>
                  ))}
                </nav>
              </div>
            </div>
            <div className="space-y-6 py-6 px-5">
              <div className="grid grid-cols-2 gap-y-4 gap-x-8">
                <a href="#" className="text-base font-medium text-gray-900 hover:text-gray-700">
                  Pricing
                </a>

                <a href="#" className="text-base font-medium text-gray-900 hover:text-gray-700">
                  Documentos
                </a>
                {resources.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    className="text-base font-medium text-gray-900 hover:text-gray-700"
                  >
                    {item.name}
                  </a>
                ))}
              </div>
              
            </div>
          </div>
        </Popover.Panel>
      </Transition>
    </Popover>
  )
}
export default CompNavBarAdmin