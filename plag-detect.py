from tkinter import *
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources (run once)
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Tokenize the text and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    return set(filtered_tokens)

def calculate_cosine_similarity(words_file1, words_file2):
    # Calculate Cosine Similarity
    intersection = len(words_file1.intersection(words_file2))
    magnitude_file1 = len(words_file1)
    magnitude_file2 = len(words_file2)

    cosine_similarity = intersection / ((magnitude_file1 * magnitude_file2) ** 0.5) if magnitude_file1 * magnitude_file2 != 0 else 0
    return cosine_similarity

def calculate_jaccard_similarity(words_file1, words_file2):
    # Calculate Jaccard Similarity
    jaccard_similarity = len(words_file1.intersection(words_file2)) / len(words_file1.union(words_file2)) if len(words_file1.union(words_file2)) != 0 else 0
    return jaccard_similarity

def calculate_combined_similarity(files):
    plagiarism_files = set()

    # Iterate over all pairs of files
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            # Read contents of each file, preprocess, and store words
            words_file1 = preprocess_text(open(files[i]).read())
            words_file2 = preprocess_text(open(files[j]).read())

            # Calculate Cosine Similarity
            cosine_similarity = calculate_cosine_similarity(words_file1, words_file2)

            # Calculate Jaccard Similarity
            jaccard_similarity = calculate_jaccard_similarity(words_file1, words_file2)

            # Average the similarities
            combined_similarity = (cosine_similarity + jaccard_similarity) / 2

            # Check if the combined similarity is above the threshold
            if combined_similarity > 0.4:
                plagiarism_files.add(files[i])
                plagiarism_files.add(files[j])

    return list(plagiarism_files)

# Example usage with three files
file_list = ['File_1.txt', 'File_2.txt', 'File_3.txt']
plagiarism_files = calculate_combined_similarity(file_list)

# Display the result using Tkinter if plagiarism files are found
if plagiarism_files:
    win = Tk()
    win.geometry("800x200")
    canvas = Canvas(win, width=700, height=650, bg="Black")
    
    result_text = "FILES WITH MORE THAN 40% COMBINED SIMILARITY:\n"
    for file_name in plagiarism_files:
        result_text += f"{file_name}\n"

    canvas.create_text(300, 100, text=result_text, fill="white", font=('Poppins-Bold'))
    canvas.pack()
    win.mainloop()
else:
    print("No files found with more than 40% combined similarity.")