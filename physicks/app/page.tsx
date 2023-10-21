import Image from "next/image";
import Link from "next/link";
import Footer from "../components/Footer";
import Features from "../components/Features";

export default function HomePage() {
  return (
  <main className="min-h-screen w-full flex flex-col items-center justify-center">
    {/* Use Cases */}
    <div className="flex items-center flex-col text-center items-center w-[70%] ">
          <div className="flex flex-col mt-8 space-y-10 ">
            <div className="text-center">
              <h1 className="font-sora text-9xl mb-8">PHYSICKS</h1>
              <h1 className="font-manrope text-6xl mt-4 text-cyan-500">Physics made easy</h1>
            </div>
            <Image
                className ="ml-[230px]"
                alt="header text"
                src="/physics_logo.png"
                width={200}
                height={200}
              />
            <div className ="mt-12">
              <h2 className ="font-sora text-5xl ">Our Story</h2>
            </div>
        </div>
    </div>
    <div className="flex flex-col bg-gray-500 bg-opacity-30 w-[70%] rounded-3xl items-center px-8 py-16 z-20 font-manrope text-xl text-center mt-4">
      <h1 className ="">
        As college students majoring in STEM, we saw ourselves struggling in physics classes, like most of our peers. It was hard to grasp the concepts, especially classical Mechanics like projectile motion — where there were too many variables to consider. There weren't many great resources to aid us in visualizing this idea.
      </h1>
      <h2 className = "mt-8 text-cyan-500">
        Enter Physicks
      </h2>
      <h1 className ="mt-8">
        Physics is a 2D projectile motion simulator that helps you visualize how 
      </h1>
    </div>
    {/* Features Title*/}
    <div className="w-full relative mt-20 text-center font-display font tracking-normal text-white-300">
      <h1 className="mb-4 font-manrope text-6xl">What it can do</h1>
      <div className="absolute top-0 mt-[-30px] right-0">
        <Image
          alt="header text"
          src="/atom.png"
          width={350}
          height={350}
        />
      </div>
      <div className="absolute bottom-0 left-0">
        <Image
          alt="header text"
          src="/Vector.png"
          width={500}
          height={500}
        />
      </div>
    </div>
    <Features />


    {/*Join*/}
    <div className ="relative flex flex-col jusitfy-center w-full">
      <div className ="flex flex-col items-center justify-center rounded-2xl mt-32 p-16">
        <h4 className = "font-sora text-7xl mb-8">What can you imagine?</h4>
        <Link
          className="bg-white rounded-lg text-black p-[16px] font-manrope text-3xl mb-4"
          href="/Python"
        >
          START FREE TRIAL
        </Link>
        <h4 className ="font-manropeR text-xl">No credit card required</h4>
      </div>
      <div className="absolute bottom-0 left-0">
        <Image
          alt="header text"
          src="/Vector.png"
          width={500}
          height={500}
        />
      </div>
    </div>

    <Footer />
  </main>
  );
}
