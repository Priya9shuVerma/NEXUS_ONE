"use client";

import { useState } from "react";
import { registerUser } from "@/services/auth";
import { useRouter } from "next/navigation";


export default function RegisterPage() {

  const router = useRouter();

  const [username,setUsername] = useState("");
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const [loading,setLoading] = useState(false);


  const handleRegister = async()=>{

    try{

      setLoading(true);


      const response = await registerUser({
      username,
        email,
        password
      });


      console.log(response);


      alert("Registration Successful");


      router.push("/login");


    }
    catch(error){

      console.log("Register Error:",error);

      alert("Registration Failed");

    }
    finally{

      setLoading(false);

    }

  };


  return (

    <main className="min-h-screen bg-black text-white flex items-center justify-center">

      <div className="w-full max-w-md bg-zinc-900 p-8 rounded-xl">


        <h1 className="text-3xl font-bold text-center mb-6">
          Create Account
        </h1>


        <input
          className="w-full p-3 mb-4 rounded bg-zinc-800"
          placeholder="Username"
          value={username}
          onChange={(e)=>setUsername(e.target.value)}
        />


        <input
          className="w-full p-3 mb-4 rounded bg-zinc-800"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        />


        <input
          className="w-full p-3 mb-4 rounded bg-zinc-800"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />


        <button
          onClick={handleRegister}
          disabled={loading}
          className="w-full bg-blue-600 p-3 rounded hover:bg-blue-700"
        >

          {
            loading ? "Creating Account..." : "Register"
          }

        </button>


      </div>


    </main>

  );

}