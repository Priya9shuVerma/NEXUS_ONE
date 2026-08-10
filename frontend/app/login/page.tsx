"use client";

import { useState } from "react";
import { loginUser } from "@/services/auth";
import { useRouter } from "next/navigation";


export default function LoginPage() {

  const router = useRouter();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [loading,setLoading] = useState(false);


  const handleLogin = async()=>{

    try{

      setLoading(true);

      const response = await loginUser({
        email,
        password
      });


      console.log(response);

      alert("Login Successful");


      router.push("/dashboard");


    }
    catch(error){

      console.log(error);

      alert("Login Failed");

    }
    finally{

      setLoading(false);

    }

  };


  return (

    <main className="min-h-screen bg-black text-white flex items-center justify-center">


      <div className="w-full max-w-md bg-zinc-900 p-8 rounded-xl">


        <h1 className="text-3xl font-bold text-center mb-6">
          NEXUS ONE Login
        </h1>


        <input
          className="w-full p-3 mb-4 rounded bg-zinc-800"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        />


        <input
          className="w-full p-3 mb-4 rounded bg-zinc-800"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />


        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-blue-600 p-3 rounded"
        >

        {
          loading ? "Logging in..." : "Login"
        }

        </button>


      </div>


    </main>

  );

}