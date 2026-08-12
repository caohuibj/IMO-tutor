# Setup

## 1. Install the Skill

Upload the folder/archive rooted at `skills/imo-tutor/` as one ChatGPT Skill.

## 2. Create a ChatGPT Project

Create a project named `IMO Tutor` (or another name) and copy `PROJECT_INSTRUCTIONS.md` into Project Instructions.

## 3. Connect Google Drive

Connect the Google Drive app. Create a private Drive folder named `IMO Tutor Data` and a Google Sheet named `IMO Learning DB`.

Create two tabs from the CSV headers in the skill references:

- `Problem_Index`
- `Attempts`

Add the Drive folder and/or Sheet as Project sources if convenient. The workflow may also discover them by their default names through the connected app.

## 4. First integration test

In a new project chat:

1. Upload one problem image.
2. Confirm the response classifies the problem but does not reveal a solution.
3. Confirm a problem record is created in `Problem_Index`.
4. Ask for H1, then H2, and confirm information is progressively disclosed.
5. Upload a handwritten solution image.
6. Confirm the image is preserved when the connector exposes an uploadable file reference, a transcription is created, and an `Attempts` row is written.
7. Finish the problem and verify the durable note/index before archiving the chat.

Raw image upload is the only connector behavior that must be validated with a real conversation attachment; the schema requires preservation of the original image reference/status even if the runtime cannot materialize it directly.

## 5. Sharing

Share this repository/release for the workflow definition. Each student should use their own ChatGPT Project and private Google Drive data store.
