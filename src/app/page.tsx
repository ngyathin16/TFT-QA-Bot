"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ChatInterface } from "@/components/chat-interface";
import { Bot, MessageCircle, X } from "lucide-react";

export default function Home() {
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="relative">
      {/* Aurora Hero Section */}
      <AuroraBackground>
        <motion.div
          initial={{ opacity: 0.0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="relative flex flex-col gap-4 items-center justify-center px-4"
        >
          <div className="text-3xl md:text-7xl font-bold dark:text-white text-center">
            TFT Set 15 Q&A Bot
          </div>
          <div className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-4 text-center">
            Your AI assistant for Teamfight Tactics knowledge
          </div>
          <div className="text-sm md:text-lg dark:text-neutral-300 text-center max-w-2xl">
            Ask questions about champions, traits, items, augments, and mechanics from TFT Set 15
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowChat(true)}
            className="bg-blue-600 hover:bg-blue-700 rounded-full w-fit text-white px-8 py-4 flex items-center space-x-3 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
          >
            <MessageCircle className="w-6 h-6" />
            <span>Start Chatting Now</span>
          </motion.button>
        </motion.div>
      </AuroraBackground>

      {/* Chat Interface Overlay */}
      {showChat && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 bg-black bg-opacity-50 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="absolute inset-4 md:inset-8 lg:inset-16"
          >
            <div className="relative h-full bg-white dark:bg-zinc-900 rounded-lg shadow-2xl overflow-hidden">
              {/* Close Button */}
              <button
                onClick={() => setShowChat(false)}
                className="absolute top-4 right-4 z-10 p-2 bg-zinc-200 dark:bg-zinc-700 rounded-full hover:bg-zinc-300 dark:hover:bg-zinc-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              
              {/* Chat Interface */}
              <ChatInterface />
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Floating Chat Button */}
      {!showChat && (
        <motion.button
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setShowChat(true)}
          className="fixed bottom-6 right-6 z-40 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
        >
          <Bot className="w-6 h-6" />
        </motion.button>
      )}
    </div>
  );
}