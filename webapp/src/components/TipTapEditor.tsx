"use client";
import React from "react";
import { EditorContent, useEditor } from "@tiptap/react";
import { StarterKit } from "@tiptap/starter-kit";
import TipTapMenuBar from "./TipTapMenuBar";
import { Button } from "./ui/button";
import type { Project } from "@prisma/client";
import { api } from "@/trpc/react";
import { useDebounce } from "./useDebounce";
import { useAtom } from "jotai";
import { projectAtom } from "./ApplicationShell";
import { RefreshCw } from "lucide-react";

type Props = { project: Project };

const TipTapEditor = ({ project }: Props) => {
  const [_, setProject] = useAtom(projectAtom);
  React.useEffect(() => {
    setProject(project);
  }, [project]);
  const saveEditor = api.project.saveNote.useMutation();
  const regenerateDoc = api.project.regenerateDocumentation.useMutation();
  const [editorState, setEditorState] = React.useState(
    project.documentation || "",
  );
  
  // Update editor state when project changes
  React.useEffect(() => {
    setEditorState(project.documentation || "");
  }, [project.documentation]);
  
  const debouncedEditorState = useDebounce(editorState, 1000); // Increased debounce time
  React.useEffect(() => {
    if (debouncedEditorState && debouncedEditorState !== project.documentation) {
      saveEditor.mutate({
        projectId: project.id,
        text: debouncedEditorState,
      });
    }
  }, [debouncedEditorState, project.documentation]);
  const editor = useEditor({
    autofocus: true,
    extensions: [StarterKit],
    content: editorState,
    onUpdate: ({ editor }) => {
      setEditorState(editor.getHTML());
    },
  });
  
  // Update editor content when editorState changes
  React.useEffect(() => {
    if (editor && editorState !== editor.getHTML()) {
      editor.commands.setContent(editorState);
    }
  }, [editorState, editor]);
  return (
    <>
      <div className="flex">
        {editor && <TipTapMenuBar editor={editor} />}
        <Button disabled variant={"outline"} className="ml-auto">
          {saveEditor.isLoading ? "Saving..." : "Saved"}
        </Button>
        {project.githubUrl && (
          <Button
            onClick={() => {
              regenerateDoc.mutate(
                { projectId: project.id },
                {
                  onSuccess: (updatedProject) => {
                    setEditorState(updatedProject.documentation || "");
                    setProject(updatedProject);
                  },
                }
              );
            }}
            disabled={regenerateDoc.isLoading}
            variant="outline"
            className="ml-2"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${regenerateDoc.isLoading ? 'animate-spin' : ''}`} />
            {regenerateDoc.isLoading ? "Regenerating..." : "Regenerate"}
          </Button>
        )}
      </div>

      <div className="prose mt-4 w-full max-w-none">
        <EditorContent editor={editor} />
      </div>
    </>
  );
};

export default TipTapEditor;
