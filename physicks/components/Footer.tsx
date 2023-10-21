import Link from "next/link";
import Image from "next/image";

export default function Footer() {
  return (
    <footer className="flex flex-col w-[90%] py-12">
      <div className ="flex flex-row justify-between border-b border-gray-700 py-10 items-center">
          <Image  className =""
              alt="header text"
              src="/head.png"
              width={260}
              height={64}
              />
        <div className ="font-manrope w-[497.41px] text-[22px] flex flex-row justify-between">
          <Link href = "https://www.decoherence.co/pricing">pricing</Link>
          <Link href ="">gallery</Link>
          <Link  href = "https://www.decoherence.co/blog">blog</Link>
          <Link  href ="https://www.decoherence.co/pricing#faq">FAQ</Link>
          <Link  href = "https://www.decoherence.co/affiliate">affiliate</Link>
        </div>
        <div className ="flex flex-row w-[18%] justify-between">
          <Link href = "https://www.decoherence.co/pricing">
            <Image 
              alt = "Twitter"
              src ="/Twitter.png"
              width = {35}
              height ={35}
              />
          </Link>
          <Link href ="">
          <Image 
              alt = "Insta"
              src ="/Insta.png"
              width = {35}
              height ={35}
              />
          </Link>
          <Link  href = "https://www.decoherence.co/blog">
          <Image 
              alt = "Tiktok"
              src ="/Tiktok.png"
              width = {35}
              height ={35}
              />
          </Link>
          <Link  href ="https://www.decoherence.co/pricing#faq">
          <Image 
              alt = "Discord"
              src ="/Discord.png"
              width = {35}
              height ={35}
              />
          </Link>
          <Link  href = "https://www.decoherence.co/affiliate">
          <Image 
              alt = "LinkedIn"
              src ="/LinkedIn.png"
              width = {35}
              height ={35}
              />
          </Link>
        </div>
      </div>
      <div className = "flex flex-row justify-between text-xl font-manropeR mt-10">
        <div className ="w-[15%] flex flex-row justify-between">
          <Link href = "https://www.ycombinator.com/companies/decoherence/jobs">career</Link>
          <Link href ="https://www.decoherence.co/terms">terms</Link>
          <Link  href = "https://www.decoherence.co/privacy">privacy</Link>
        </div>
      </div>
    </footer>
  );
}
